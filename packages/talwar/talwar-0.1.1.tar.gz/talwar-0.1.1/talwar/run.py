import argparse
import os
import sys
from talwar.agent import Agent

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║      ████████╗ █████╗ ██╗     ██╗    ██╗  █████╗ ██████╗             ║
    ║      ╚══██╔══╝██╔══██╗██║     ██║    ██║  ██╔══██╗██╔══██╗           ║
    ║         ██║   ███████║██║     ██║ █╗ ██║  ███████║██████╔╝           ║
    ║         ██║   ██╔══██║██║     ██║███╗██   ██╔══██║██╔══██╗           ║
    ║         ██║   ██║  ██║███████╗╚███╔███╔   ██║  ██║██║  ██║           ║
    ║         ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝   ╚═╝  ╚═╝╚═╝  ╚═╝           ║
    ║                                                                      ║
    ║           Automated Penetration Testing via Security Agents          ║
    ║                                                                      ║
    ║                   [+] Vulnerability discovery                        ║
    ║                   [+] Payload generation                             ║
    ║                   [+] Context-aware testing                          ║
    ║                   [+] Exploit verification                           ║
    ║                                                                      ║
    ║                     -- More to come! --                              ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def parse_args():
    parser = argparse.ArgumentParser(
        description='AI-Powered Web Application Security Testing Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    # Basic scan of a single URL
    python run.py -t https://example.com -m o3-mini -o results

    # Advanced scan with subdomain enumeration and URL discovery
    python run.py -t https://example.com -e -s -m o3-preview -i 10
        '''
    )
    
    parser.add_argument('-t', '--target', 
                        required=True,
                        help='Target URL to test')

    parser.add_argument('-e', '--expand',
                        action='store_true',
                        default=False,
                        help='Expand testing to discovered URLs')
    
    parser.add_argument('-s', '--subdomains',
                        action='store_true',
                        default=False,
                        help='Perform subdomain enumeration')

    parser.add_argument('-m', '--model',
                        choices=['o3-mini', 'o1-preview'],
                        default='o3-mini',
                        help='LLM model to use (default: o3-mini)')
    
    parser.add_argument('-o', '--output',
                        default='pentest_report',
                        help='Output directory for results (default: pentest_report)')
    
    parser.add_argument('-i', '--max-iterations',
                        type=int,
                        default=10,
                        help='Maximum iterations per plan of attack (default: 10)')

    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    return args

def execute(args):
    """Execute the security scan with the given arguments"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(args.output, exist_ok=True)
        
        # Initialize and run the agent
        agent = Agent(
            starting_url=args.target,
            output_dir=args.output,
            model=args.model,
            max_iterations=args.max_iterations,
            expand_scope=args.expand,
            enumerate_subdomains=args.subdomains
        )
        
        print("\n[*] Initiating security scan...")
        print(f"[*] Target URL: {args.target}")
        print(f"[*] Using model: {args.model}")
        print(f"[*] Results will be saved to: {args.output}\n")
        
        agent.run()
        
    except Exception as e:
        if "Executable doesn't exist" in str(e):
            print("\n[!] Error: Playwright browser is not installed.")
            print("[!] Please run the following command to install it:")
            print("    playwright install chromium")
            print("\n[!] Then try running talwar again.")
        else:
            print(f"\n[!] Error: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point for the CLI"""
    # Print banner first, before any other output
    print_banner()
    
    # Parse command line arguments
    args = parse_args()
    
    # Execute the scan
    execute(args)

# Always print banner when module is imported
print_banner()

# Execute main() when script is run directly
if __name__ == "__main__":
    main()