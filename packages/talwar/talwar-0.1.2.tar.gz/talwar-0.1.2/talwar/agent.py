import os
import json
import time
import base64
import logging
from typing import Dict, List, Optional, Any
from talwar.logger import Logger
from talwar.proxy import WebProxy
from talwar.llm import LLM
from talwar.scanner import Scanner
from talwar.parser import HTMLParser
from talwar.planner import Planner
from talwar.tools import Tools
from talwar.summarizer import Summarizer
from talwar.utils import check_hostname, enumerate_subdomains, wait_for_network_idle, count_tokens
from talwar.reporter import Reporter

logger = Logger()

class Agent:
    """
    AI-powered security testing agent that scans web applications for vulnerabilities.
    
    The agent uses an LLM to intelligently analyze web pages, generate test plans,
    and execute security tests using various tools. It monitors network traffic,
    evaluates responses, and generates detailed vulnerability reports.
    """

    def __init__(self, starting_url: str, expand_scope: bool = False, 
                 enumerate_subdomains: bool = False, model: str = 'o3-mini',
                 output_dir: str = 'pentest_report', max_iterations: int = 10,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the security testing agent.

        Args:
            starting_url: Base URL to begin scanning from
            expand_scope: Whether to scan additional discovered URLs
            enumerate_subdomains: Whether to discover and scan subdomains
            model: LLM model to use for analysis
            output_dir: Directory to save scan results
            max_iterations: Maximum iterations per test plan
            config: Additional configuration options
        """
        self.starting_url = starting_url
        self.expand_scope = expand_scope
        self.should_enumerate_subdomains = enumerate_subdomains
        self.model = model
        self.output_dir = output_dir
        self.max_iterations = max_iterations
        self.keep_messages = 15
        self.config = config or {}
        
        # Initialize components
        self.proxy = WebProxy(starting_url, logger)
        self.llm = LLM()
        self.planner = Planner()
        self.scanner = None
        self.tools = Tools(config=self.config)
        self.history = []
        self.reporter = Reporter(starting_url, output_dir=output_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def _handle_error(self, error: Exception, context: str):
        """Handle errors during scanning with appropriate logging and recovery."""
        logger.error(f"Error in {context}: {str(error)}", color='red')
        
        # Implement error recovery strategies based on error type
        if isinstance(error, ConnectionError):
            logger.warning("Connection error detected, retrying after delay...", color='yellow')
            time.sleep(5)
            return True  # Retry operation
        elif isinstance(error, TimeoutError):
            logger.warning("Timeout detected, continuing with next URL...", color='yellow')
            return False  # Skip current operation
        else:
            logger.error("Unrecoverable error, exiting...", color='red')
            raise error

    def run(self):
        """
        Execute the security scan with improved error handling.
        """
        try:
            # Create web proxy to monitor all requests
            logger.info("Creating web proxy to monitor requests", color='yellow')
            browser, context, page, playwright = self.proxy.create_proxy()
            
            # Initialize URL queue
            urls_to_parse = [self.starting_url]
            if self.should_enumerate_subdomains:
                logger.info("Enumerating subdomains, might take a few minutes", color='yellow')
                subdomains = enumerate_subdomains(self.starting_url)
                urls_to_parse.extend(subdomains)
            
            total_urls = len(urls_to_parse)
            completed_urls = set()
            
            # Initialize scanner
            logger.info("Extracting page contents", color='yellow')
            self.scanner = Scanner(page)

            total_tokens = 0
            current_url_index = 0
            
            while urls_to_parse:
                try:
                    # Visit the URL and start scanning it
                    url = urls_to_parse.pop(0)
                    current_url_index += 1
                    
                    logger.info(f"Starting scan: {url} ({current_url_index}/{total_urls})", color='cyan')
                    
                    scan_results = self.scanner.scan(url)
                    completed_urls.add(url)

                    # Add URLs to queue if expand_scope is enabled
                    if self.expand_scope:
                        more_urls = scan_results["parsed_data"]["urls"]
                        new_urls = 0
                        for _url in more_urls:
                            _url = _url["href"]
                            if (_url not in urls_to_parse and 
                                _url not in completed_urls and 
                                check_hostname(self.starting_url, _url)):
                                urls_to_parse.append(_url)
                                new_urls += 1
                                total_urls += 1
                        if new_urls > 0:
                            logger.info(f"Added {new_urls} new URLs to the search queue", color='green')

                    # Build a plan for what we should try for this page
                    page_source = scan_results["html_content"]
                    total_tokens += count_tokens(page_source)
                    page_source = Summarizer().summarize_page_source(page_source, url)
                    page_data = f"Page information: {page_source}\n*** URL of the page we are planning for: {url} ***"

                    # Initialize history with system prompt and page data
                    self.history = [
                        {"role": "system", "content": self.llm.system_prompt},
                        {"role": "user", "content": page_data}
                    ]
                    
                    # Generate and execute test plans
                    plans = self.planner.plan(page_data)
                    total_plans = len(plans)
                    
                    # Display all plans upfront
                    logger.info("Generated Security Testing Plan:", color='yellow')
                    for index, plan in enumerate(plans):
                        logger.info(f"Plan {index + 1}/{total_plans}: {plan['title']}", color='light_magenta')
                        logger.info(f"Description: {plan['description']}", color='white')
                        logger.info("---", color='white')
                    
                    # Execute plans
                    for index, plan in enumerate(plans):
                        logger.info(f"Executing Plan {index + 1}/{total_plans}: {plan['title']}", color='light_magenta')
                        self._execute_plan(plan, page, index, total_plans)
                    
                except Exception as e:
                    if not self._handle_error(e, f"scanning URL {url}"):
                        continue

            # Generate final report
            logger.info("Generating summary report", color='yellow')
            self.reporter.generate_summary_report()
            
        except Exception as e:
            logger.error(f"Fatal error during scan: {str(e)}", color='red')
            raise

    def _execute_plan(self, plan: Dict[str, str], page, plan_index: int, total_plans: int):
        """Execute a single test plan with error handling."""
        try:
            # Reset history when starting a new plan
            self.history = self.history[:2]
            
            logger.info(f"Executing plan {plan_index + 1}/{total_plans}: {plan['title']}", color='cyan')
            self.history.append({"role": "assistant", "content": f"I will now start exploring the ```{plan['title']} - {plan['description']}``` and see if I can find any issues around it. Are we good to go?"})
            self.history.append({"role": "user", "content": "Sure, let us start exploring this by trying out some tools. We must stick to the plan and do not deviate from it. Once we are done, simply call the completed function."})
            
            iterations = 0
            while iterations < self.max_iterations:
                try:
                    # Manage history size
                    if len(self.history) > self.keep_messages:
                        keep_from_end = self.keep_messages - 4
                        self.history = self.history[:4] + Summarizer().summarize_conversation(self.history[4:-keep_from_end]) + self.history[-keep_from_end:]
                    
                    # Execute LLM reasoning
                    plan_tokens = count_tokens(self.history)
                    logger.info(f"Current query tokens: {plan_tokens:,}", color='red')
                    
                    llm_response = self.llm.reason(self.history)
                    self.history.append({"role": "assistant", "content": llm_response})
                    logger.info(f"{llm_response}", color='light_blue')

                    # Extract and execute tool use
                    tool_use = self.tools.extract_tool_use(llm_response)
                    logger.info(f"{tool_use}", color='yellow')

                    tool_output = str(self.tools.execute_tool(page, tool_use))
                    logger.info(f"{tool_output[:250]}{'...' if len(tool_output) > 250 else ''}", color='yellow')
                    
                    tool_output_summarized = Summarizer().summarize(llm_response, tool_use, tool_output)
                    self.history.append({"role": "user", "content": tool_output_summarized})
                    logger.info(f"{tool_output_summarized}", color='cyan')       

                    if tool_output == "Completed":
                        successful_exploit, report = self.reporter.report(self.history[2:])
                        logger.info(f"Analysis of the issue the agent has found: {report}", color='green')
                        
                        if successful_exploit:
                            logger.info("Completed, moving onto the next plan!", color='yellow')
                            break
                        else:
                            logger.info("Need to work harder on the exploit.", color='red')
                            self.history.append({"role": "user", "content": report + "\n. Lets do better, again!"})
                    
                    # Monitor traffic
                    wait_for_network_idle(page)
                    traffic = self.proxy.pretty_print_traffic()
                    if traffic:
                        logger.info(traffic, color='cyan')
                        self.history.append({"role": "user", "content": traffic})
                    self.proxy.clear()

                    iterations += 1
                    if iterations >= self.max_iterations:
                        logger.info("Max iterations reached, moving onto the next plan!", color='red')
                        break
                        
                except Exception as e:
                    if not self._handle_error(e, f"executing plan {plan['title']}"):
                        break
                        
        except Exception as e:
            self._handle_error(e, f"executing plan {plan['title']}")