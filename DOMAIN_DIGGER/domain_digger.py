#!/usr/bin/env python3
"""
███████╗██╗  ██╗███████╗██████╗ ███████╗██████╗ ███████╗
██╔════╝██╗  ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝
███████╗███████║█████╗  ██████╔╝█████╗  ██████╔╝███████╗
╚════██║██╔══██║██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║
███████║██║  ██║███████╗██║  ██║███████╗██║  ██║███████║
╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
        DOMAIN DIGGER MEGA SCANNER WITH LOADER + CLEAN EXIT
        BY NU11SECUR1TY 2026
"""

import requests
import socket
import json
import sys
import time
import argparse
import threading
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse
import ssl
import itertools
import string
import ipaddress
import re
import os
import signal
from collections import defaultdict, Counter
import random
import hashlib

# ========== LOADER CLASSES ==========
class Loader:
    """Beautiful loader animations"""
    def __init__(self, message="Loading", delay=0.1):
        self.message = message
        self.delay = delay
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the loader"""
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the loader"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
        sys.stdout.write("\r" + " " * (len(self.message) + 30) + "\r")
        sys.stdout.flush()
        
    def _animate(self):
        """Loader animation"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]
        i = 0
        
        while self.running:
            frame = frames[i % len(frames)]
            color = colors[i % len(colors)]
            sys.stdout.write(f"\r{color}{frame}\033[0m {self.message}... ")
            sys.stdout.flush()
            time.sleep(self.delay)
            i += 1

class ProgressBar:
    """Progress bar with stats"""
    def __init__(self, total, description="Progress"):
        self.total = total
        self.description = description
        self.current = 0
        self.start_time = time.time()
        self.width = 40
        
    def update(self, value):
        """Update progress"""
        self.current = value
        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = "█" * filled + "░" * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        if self.current > 0 and elapsed > 0:
            rate = self.current / elapsed
            eta = (self.total - self.current) / rate if rate > 0 else 0
            
            sys.stdout.write(f"\r\033[92m[{bar}]\033[0m {percent:.1%} | "
                           f"{self.current:,}/{self.total:,} | "
                           f"{rate:.1f}/sec | ETA: {self._format_time(eta)}")
            sys.stdout.flush()
            
    def finish(self):
        """Finish progress bar"""
        elapsed = time.time() - self.start_time
        sys.stdout.write(f"\r\033[92m[{'█' * self.width}]\033[0m 100% | "
                       f"{self.total:,}/{self.total:,} | "
                       f"Time: {self._format_time(elapsed)}\n")
        sys.stdout.flush()
        
    def _format_time(self, seconds):
        """Format seconds to readable time"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.0f}m {seconds%60:.0f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"

class StatusMonitor:
    """Real-time status monitor"""
    def __init__(self):
        self.lines = {}
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._display, daemon=True)
        
    def start(self):
        """Start monitor"""
        self.thread.start()
        
    def stop(self):
        """Stop monitor"""
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1)
        self.clear()
        
    def update(self, key, value):
        """Update a status line"""
        with self.lock:
            self.lines[key] = value
            
    def clear(self):
        """Clear display"""
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        
    def _display(self):
        """Display loop"""
        while self.running:
            with self.lock:
                if self.lines:
                    sys.stdout.write("\033[2J\033[H")
                    print("\033[96m" + "="*60 + "\033[0m")
                    print("\033[95m" + " " * 20 + "SCAN STATUS" + " " * 20 + "\033[0m")
                    print("\033[96m" + "="*60 + "\033[0m")
                    
                    for key, value in sorted(self.lines.items()):
                        print(f"\033[93m{key:25}\033[0m: {value}")
                    
                    print("\033[96m" + "="*60 + "\033[0m")
                    print("\033[90mPress Ctrl+C for clean exit...\033[0m")
            
            time.sleep(0.5)

# ========== ENHANCED EXIT HANDLER ==========
class ExitHandler:
    """Handle clean exits with Ctrl+C"""
    def __init__(self):
        self.exit_requested = False
        self.loaders = []
        self.monitors = []
        self.callbacks = []
        signal.signal(signal.SIGINT, self._signal_handler)
        self.original_sigint = signal.getsignal(signal.SIGINT)
        
    def register_loader(self, loader):
        """Register a loader to stop on exit"""
        self.loaders.append(loader)
        
    def register_monitor(self, monitor):
        """Register a monitor to stop on exit"""
        self.monitors.append(monitor)
        
    def register_callback(self, callback):
        """Register a callback to run on exit"""
        self.callbacks.append(callback)
        
    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C - IMMEDIATE EXIT"""
        if not self.exit_requested:
            self.exit_requested = True
            print("\n\n\033[93m[!] Exit requested. Exiting immediately...\033[0m")
            
            # Run callbacks first (for cleanup)
            for callback in self.callbacks:
                try:
                    callback()
                except:
                    pass
                    
            # Stop all loaders
            for loader in self.loaders:
                loader.stop()
                
            # Stop all monitors
            for monitor in self.monitors:
                monitor.stop()
                
            print("\033[92m[✓] Immediate exit completed\033[0m")
            os._exit(1)  # IMMEDIATE EXIT - CHANGED FROM sys.exit(0)
            
    def restore_signal(self):
        """Restore original signal handler"""
        signal.signal(signal.SIGINT, self.original_sigint)

# ========== CONFIGURATION ==========
class MegaConfig:
    TIMEOUT = 4
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    MAX_WORKERS = 30
    RATE_LIMIT = 0.05
    COUNTER_MAX = 1000000
    MAX_DOMAINS = 5000000
    BATCH_SIZE = 5000

# ========== THREADING LOCKS ==========
print_lock = threading.Lock()
results_lock = threading.Lock()
counter_lock = threading.Lock()
stats_lock = threading.Lock()

# ========== DATASETS ==========
class MegaDatasets:
    # ALL COUNTRIES TLDs (250+)
    ALL_COUNTRIES = [
        '.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.ao', '.aq', '.ar',
        '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf',
        '.bg', '.bh', '.bi', '.bj', '.bm', '.bn', '.bo', '.bq', '.br', '.bs', '.bt',
        '.bv', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci',
        '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', '.cw', '.cx', '.cy',
        '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.ee', '.eg', '.eh',
        '.er', '.es', '.et', '.eu', '.fi', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga',
        '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gp',
        '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr',
        '.ht', '.hu', '.id', '.ie', '.il', '.im', '.in', '.io', '.iq', '.ir', '.is',
        '.it', '.je', '.jm', '.jo', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn',
        '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr',
        '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.me', '.mg', '.mh',
        '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu',
        '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni',
        '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg',
        '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', '.py', '.qa',
        '.re', '.ro', '.rs', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg',
        '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.ss', '.st',
        '.su', '.sv', '.sx', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj',
        '.tk', '.tl', '.tm', '.tn', '.to', '.tr', '.tt', '.tv', '.tw', '.tz', '.ua',
        '.ug', '.uk', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn',
        '.vu', '.wf', '.ws', '.ye', '.yt', '.za', '.zm', '.zw',
    ]
    
    # ALL GENERIC TLDs
    ALL_GENERIC = [
        '.com', '.net', '.org', '.info', '.biz', '.xyz', '.online', '.site', '.tech',
        '.store', '.shop', '.app', '.dev', '.io', '.ai', '.co', '.me', '.tv', '.fm',
        '.name', '.pro', '.mobi', '.tel', '.asia', '.cat', '.jobs', '.travel', '.post',
        '.aero', '.coop', '.museum', '.int', '.mil', '.gov', '.edu',
    ]
    
    ALL_SUBDOMAINS = []
    
    @staticmethod
    def load_all_subs():
        """Generate subdomain prefixes"""
        if MegaDatasets.ALL_SUBDOMAINS:
            return MegaDatasets.ALL_SUBDOMAINS
        
        subs = set()
        
        # Common words
        common_words = [
            'www', 'mail', 'ftp', 'api', 'blog', 'admin', 'portal', 'app', 'dev', 'test',
            'staging', 'secure', 'vpn', 'mx', 'ns1', 'ns2', 'web', 'cloud', 'cdn', 'forum',
            'shop', 'store', 'support', 'help', 'docs', 'status', 'monitor', 'news',
            'community', 'chat', 'wiki', 'kb', 'download', 'upload', 'files', 'media',
        ]
        
        subs.update(common_words)
        
        # Single letters
        subs.update([chr(i) for i in range(ord('a'), ord('z')+1)])
        
        # Double letters
        for c1 in string.ascii_lowercase:
            for c2 in string.ascii_lowercase:
                subs.add(c1 + c2)
        
        # Numbers
        subs.update([str(i) for i in range(100)])
        
        MegaDatasets.ALL_SUBDOMAINS = list(subs)
        return MegaDatasets.ALL_SUBDOMAINS

# ========== DOMAIN GENERATOR ==========
class MegaGenerator:
    def __init__(self, base_name):
        self.base_name = base_name.lower()
        self.generated_count = 0
        
    def generate_for_counter(self, counter_value):
        """Generate domains for specific counter value"""
        domains = []
        
        # Base patterns - NOW WITH NUMBERS IN FRONT
        patterns = [
            # NUMBERS IN FRONT (NEW!) - e.g., 1tempobet.com, 2tempobet.com
            f"{counter_value}{self.base_name}.com",
            f"{counter_value}{self.base_name}.net",
            f"{counter_value}{self.base_name}.org",
            f"{counter_value}-{self.base_name}.com",
            f"{counter_value}.{self.base_name}.com",
            
            # Original patterns (numbers after) - e.g., tempobet1.com, tempobet2.com
            f"{self.base_name}{counter_value}.com",
            f"{self.base_name}{counter_value}.net",
            f"{self.base_name}{counter_value}.org",
            f"{self.base_name}-{counter_value}.com",
            f"{self.base_name}.{counter_value}.com",
        ]
        
        # Add TLD variations for BOTH patterns
        for tld in ['.com', '.net', '.org', '.io']:
            # Numbers in front variations
            patterns.append(f"{counter_value}{self.base_name}{tld}")
            patterns.append(f"{counter_value}-{self.base_name}{tld}")
            
            # Numbers after variations
            patterns.append(f"{self.base_name}{counter_value}{tld}")
            patterns.append(f"{self.base_name}-{counter_value}{tld}")
        
        # Add subdomain variations for BOTH patterns
        for sub in ['www', 'api', 'app', 'mail']:
            # Numbers in front with subdomain
            patterns.append(f"{sub}.{counter_value}{self.base_name}.com")
            patterns.append(f"{sub}.{counter_value}-{self.base_name}.com")
            
            # Numbers after with subdomain
            patterns.append(f"{sub}.{self.base_name}{counter_value}.com")
            patterns.append(f"{sub}.{self.base_name}-{counter_value}.com")
        
        return list(set(patterns))

# ========== HYPER SCANNER ==========
class HyperScanner:
    def __init__(self, base_name):
        self.base_name = base_name
        self.generator = MegaGenerator(base_name)
        self.results = []
        self.stats = {
            'total_generated': 0,
            'total_checked': 0,
            'total_found': 0,
            'by_counter': defaultdict(int),
            'by_tld': defaultdict(int),
            'by_sub': defaultdict(int),
            'start_time': time.time(),
        }
        
        # Initialize components
        self.loader = Loader("Scanning domains")
        self.monitor = StatusMonitor()
        self.progress = None
        
        # Setup exit handler
        self.exit_handler = ExitHandler()
        self.exit_handler.register_loader(self.loader)
        self.exit_handler.register_monitor(self.monitor)
        self.exit_handler.register_callback(self._cleanup_callback)
    
    def _cleanup_callback(self):
        """Cleanup callback for exit handler"""
        self.save_progress(f"{self.base_name}_interrupted.json")
        
    def check_domain(self, domain):
        """Check a single domain"""
        result = {
            'domain': domain,
            'exists': False,
            'counter': None,
            'subdomain': None,
            'tld': None,
            'response_time': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract info
        if '.' in domain:
            parts = domain.split('.')
            if len(parts) >= 2:
                result['tld'] = f".{parts[-1]}"
                # Try to find counter
                name_part = '.'.join(parts[:-1])
                numbers = re.findall(r'\d+', name_part)
                if numbers:
                    result['counter'] = int(numbers[-1])
                
                # Check if has subdomain
                if len(parts) >= 3:
                    result['subdomain'] = parts[0]
        
        # DNS check
        start = time.time()
        try:
            # Set timeout to prevent hanging
            socket.setdefaulttimeout(MegaConfig.TIMEOUT)
            ip = socket.gethostbyname(domain)
            result['exists'] = True
            result['ip'] = ip
            result['response_time'] = round((time.time() - start) * 1000, 2)
            
        except (socket.gaierror, socket.timeout):
            pass
        except Exception:
            pass
        
        return result
    
    def scan_batch(self, domains_batch):
        """Scan a batch of domains"""
        batch_results = []
        
        # Update monitor
        self.monitor.update("Current Batch", f"{len(domains_batch):,} domains")
        self.monitor.update("Workers Active", f"{MegaConfig.MAX_WORKERS}")
        
        # Multi-threaded scanning with ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=MegaConfig.MAX_WORKERS,
            thread_name_prefix="Scanner"
        ) as executor:
            
            future_to_domain = {
                executor.submit(self.check_domain, domain): domain 
                for domain in domains_batch
            }
            
            completed = 0
            for future in concurrent.futures.as_completed(future_to_domain):
                # Check for exit request before processing
                if self.exit_handler.exit_requested:
                    break
                    
                domain = future_to_domain[future]
                try:
                    result = future.result(timeout=MegaConfig.TIMEOUT + 1)
                    batch_results.append(result)
                    completed += 1
                    
                    # Update progress
                    if self.progress:
                        self.progress.update(completed)
                    
                    # Update stats
                    with stats_lock:
                        self.stats['total_checked'] += 1
                        if result['exists']:
                            self.stats['total_found'] += 1
                            if result['counter']:
                                self.stats['by_counter'][result['counter']] += 1
                            if result['tld']:
                                self.stats['by_tld'][result['tld']] += 1
                            if result['subdomain']:
                                self.stats['by_sub'][result['subdomain']] += 1
                    
                    # Update monitor stats
                    elapsed = time.time() - self.stats['start_time']
                    rate = self.stats['total_checked'] / elapsed if elapsed > 0 else 0
                    
                    self.monitor.update("Total Checked", f"{self.stats['total_checked']:,}")
                    self.monitor.update("Total Found", f"{self.stats['total_found']:,}")
                    
                    success_rate = (
                        self.stats['total_found'] / self.stats['total_checked'] * 100 
                        if self.stats['total_checked'] > 0 else 0
                    )
                    self.monitor.update("Success Rate", f"{success_rate:.2f}%")
                    
                    self.monitor.update("Rate", f"{rate:.1f} domains/sec")
                    self.monitor.update("Elapsed Time", self._format_time(elapsed))
                    
                except concurrent.futures.TimeoutError:
                    pass
                except Exception:
                    pass
        
        return batch_results
    
    def run_full_scan(self, max_counter=100000):
        """Run full mega scan"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    HYPER SCAN WITH LOADER                    ║
║                    TARGET: {self.base_name:30}               ║
║                    COUNTER RANGE: 1-{max_counter:12,}        ║
║                    WORKERS: {MegaConfig.MAX_WORKERS:12}      ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Start loaders and monitor
        self.loader.start()
        self.monitor.start()
        
        time.sleep(1)  # Show loader briefly
        
        # Estimate total domains
        domains_per_counter = 20  # Increased because we now have MORE patterns
        total_domains = min(max_counter * domains_per_counter, MegaConfig.MAX_DOMAINS)
        
        print(f"\n[+] Estimated total domains: {total_domains:,}")
        print("[+] Starting scan with real-time monitoring...")
        print("[+] Press Ctrl+C at any time for clean exit\n")
        
        # Initialize progress bar
        self.progress = ProgressBar(total_domains, "Scan Progress")
        
        try:
            # Scan by counter batches
            batch_size = MegaConfig.BATCH_SIZE
            
            for batch_start in range(1, max_counter + 1, batch_size):
                if self.exit_handler.exit_requested:
                    break
                    
                batch_end = min(batch_start + batch_size - 1, max_counter)
                
                # Update monitor
                self.monitor.update("Current Range", f"{batch_start:,} - {batch_end:,}")
                
                # Generate domains for this counter batch
                batch_domains = []
                for counter in range(batch_start, batch_end + 1):
                    if self.exit_handler.exit_requested:
                        break
                    counter_domains = self.generator.generate_for_counter(counter)
                    batch_domains.extend(counter_domains[:15])  # Limit per counter
                
                # Scan batch if we have domains and exit not requested
                if batch_domains and not self.exit_handler.exit_requested:
                    batch_results = self.scan_batch(batch_domains)
                    self.results.extend(batch_results)
                    
                    # Save progress every batch for better recovery
                    if batch_start % batch_size == 0:
                        self.save_progress()
            
        finally:
            # Ensure cleanup happens
            self.loader.stop()
            self.monitor.stop()
            
            if self.progress:
                self.progress.finish()
        
        return self.generate_report()
    
    def save_progress(self, filename=None):
        """Save progress to file"""
        if not filename:
            filename = f"{self.base_name}_scan_progress.json"
        
        try:
            report = {
                'target': self.base_name,
                'timestamp': datetime.now().isoformat(),
                'stats': dict(self.stats),
                'found_domains': [
                    {
                        'domain': r['domain'],
                        'counter': r.get('counter'),
                        'ip': r.get('ip'),
                        'tld': r.get('tld')
                    }
                    for r in self.results if r['exists']
                ],
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
                
            self.monitor.update("Last Save", datetime.now().strftime("%H:%M:%S"))
            
        except Exception:
            pass
    
    def generate_report(self):
        """Generate final report"""
        elapsed = time.time() - self.stats['start_time']
        
        report = {
            'metadata': {
                'target': self.base_name,
                'scan_start': datetime.fromtimestamp(self.stats['start_time']).isoformat(),
                'scan_end': datetime.now().isoformat(),
                'duration_seconds': round(elapsed, 2),
                'duration_human': self._format_time(elapsed),
                'domains_per_second': round(self.stats['total_checked'] / elapsed, 2) if elapsed > 0 else 0,
            },
            'statistics': {
                'total_checked': self.stats['total_checked'],
                'total_found': self.stats['total_found'],
                'success_rate': f"{(self.stats['total_found'] / self.stats['total_checked'] * 100):.4f}%" 
                               if self.stats['total_checked'] > 0 else "0%",
            },
            'found_domains': [
                {
                    'domain': r['domain'],
                    'ip': r.get('ip'),
                    'counter': r.get('counter'),
                    'subdomain': r.get('subdomain'),
                    'tld': r.get('tld'),
                }
                for r in self.results if r['exists']
            ],
        }
        
        return report
    
    def _format_time(self, seconds):
        """Format seconds to readable time"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"

# ========== MAIN ==========
def main():
    parser = argparse.ArgumentParser(
        description='MEGA SCANNER WITH LOADER + CLEAN EXIT',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python megascan_loader.py tempobet --counter 100000
  python megascan_loader.py google --workers 30
  python megascan_loader.py microsoft --output results.json
        """
    )
    
    parser.add_argument('target', help='Target name to scan')
    parser.add_argument('--counter', type=int, default=10000, 
                       help='Max counter value (default: 10000)')
    parser.add_argument('--output', help='Output JSON file')
    parser.add_argument('--workers', type=int, default=30,
                       help='Number of workers (default: 30)')
    parser.add_argument('--batch', type=int, default=5000,
                       help='Batch size (default: 5000)')
    
    args = parser.parse_args()
    
    # Update config
    MegaConfig.MAX_WORKERS = args.workers
    MegaConfig.BATCH_SIZE = args.batch
    MegaConfig.COUNTER_MAX = args.counter
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  MEGA SCANNER v4.0 - LOADER                  ║
║                    Target: {args.target:30}               ║
║                    Counter: 1-{args.counter:12,}                  ║
║                    Workers: {args.workers:12}                   ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"[+] Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[+] Press Ctrl+C at any time for clean exit with progress save")
    print("-" * 60)
    
    # Initialize scanner
    scanner = HyperScanner(args.target)
    
    try:
        # Run scan
        report = scanner.run_full_scan(max_counter=args.counter)
        
        # Display results
        print(f"\n{'='*60}")
        print("\033[95mSCAN COMPLETE\033[0m")
        print(f"{'='*60}")
        print(f"Target: \033[93m{args.target}\033[0m")
        print(f"Duration: \033[92m{report['metadata']['duration_human']}\033[0m")
        print(f"Domains checked: \033[96m{report['statistics']['total_checked']:,}\033[0m")
        print(f"Domains found: \033[92m{report['statistics']['total_found']:,}\033[0m")
        print(f"Success rate: \033[95m{report['statistics']['success_rate']}\033[0m")
        print(f"Rate: \033[93m{report['metadata']['domains_per_second']:.1f} domains/sec\033[0m")
        
        if report['statistics']['total_found'] > 0:
            print(f"\n\033[92m[+] FOUND DOMAINS:\033[0m")
            for i, domain in enumerate(report['found_domains'][:10], 1):
                print(f"  {i:2}. \033[96m{domain['domain']}\033[0m")
                if domain.get('ip'):
                    print(f"      IP: {domain['ip']}")
            
            if len(report['found_domains']) > 10:
                print(f"  ... and {len(report['found_domains']) - 10} more")
        
        # Save output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n\033[92m[✓] Full report saved to: {args.output}\033[0m")
        
        # Auto-save
        auto_file = f"{args.target}_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        scanner.save_progress(auto_file)
        print(f"\033[92m[✓] Auto-saved to: {auto_file}\033[0m")
        
    except KeyboardInterrupt:
        # Already handled by ExitHandler
        pass
    except Exception as e:
        print(f"\n\033[91m[!] Error: {e}\033[0m")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
