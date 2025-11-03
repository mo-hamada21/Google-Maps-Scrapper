import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import pandas as pd
from datetime import datetime, timedelta
import re
import os
from pathlib import Path
import threading
from tkinter import font
import json

# Import from your scraper script
try:
    from google_maps_scraper import (
        scrape_reviews_function,
        process_reviews_function,
        save_reviews_function,
        detect_review_language,
        GoogleMapsReviewScraper,
        ReviewTextProcessor
    )
    SCRAPER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import scraper functions: {e}")
    SCRAPER_AVAILABLE = False


class ReviewAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Maps Review Analyzer & Scraper")
        self.root.geometry("1000x800")
        self.root.configure(bg='#f0f0f0')

        # Data storage
        self.reviews_df = None
        self.filtered_reviews = None
        self.all_reviews = []

        # Configure style
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        """Setup custom styles for the GUI"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Custom colors
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        self.style.configure('Custom.TButton', font=('Arial', 10, 'bold'))

    def setup_ui(self):
        """Setup the GUI interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Scrape New Reviews
        self.setup_scraper_tab()

        # Tab 2: Analyze Existing Reviews
        self.setup_analyzer_tab()

    def setup_scraper_tab(self):
        """Setup the review scraping tab"""
        scraper_frame = ttk.Frame(self.notebook)
        self.notebook.add(scraper_frame, text="Scrape Reviews")

        # Title
        title_label = ttk.Label(scraper_frame, text="Google Maps Review Scraper", style='Title.TLabel')
        title_label.pack(pady=(10, 20))

        # Input frame
        input_frame = ttk.LabelFrame(scraper_frame, text="Scraping Parameters", padding="15")
        input_frame.pack(fill='x', padx=20, pady=10)

        # URL input
        ttk.Label(input_frame, text="Google Maps Place URL:", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
        self.url_entry = ttk.Entry(input_frame, font=('Arial', 10), width=80)
        self.url_entry.pack(fill='x', pady=(0, 15))

        # Number of reviews
        reviews_frame = ttk.Frame(input_frame)
        reviews_frame.pack(fill='x', pady=(0, 15))

        ttk.Label(reviews_frame, text="Number of Reviews:", style='Header.TLabel').pack(side='left')
        self.num_reviews_var = tk.StringVar(value="50")
        self.num_reviews_spinbox = ttk.Spinbox(reviews_frame, from_=1, to=10000, textvariable=self.num_reviews_var, width=10)
        self.num_reviews_spinbox.pack(side='left', padx=(10, 0))

        # Scrape button
        self.scrape_button = ttk.Button(input_frame, text="Start Scraping",
                                       command=self.start_scraping, style='Custom.TButton')
        self.scrape_button.pack(pady=(10, 0))

        # Progress bar
        self.progress_var = tk.StringVar(value="Ready to scrape...")
        ttk.Label(input_frame, textvariable=self.progress_var).pack(pady=(10, 0))

        self.progress_bar = ttk.Progressbar(input_frame, mode='indeterminate')
        self.progress_bar.pack(fill='x', pady=(5, 0))

        # Results frame
        results_frame = ttk.LabelFrame(scraper_frame, text="Scraped Reviews", padding="15")
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Reviews text display
        self.scraped_text = scrolledtext.ScrolledText(results_frame, height=15, width=80,
                                                     font=('Arial', 9), wrap=tk.WORD)
        self.scraped_text.pack(fill='both', expand=True, pady=(0, 10))

        # Save buttons frame
        save_frame = ttk.Frame(results_frame)
        save_frame.pack(fill='x')

        ttk.Button(save_frame, text="Save to CSV", command=self.save_scraped_reviews).pack(side='left', padx=(0, 10))
        ttk.Button(save_frame, text="Use for Analysis", command=self.use_for_analysis).pack(side='left')

    def setup_analyzer_tab(self):
        """Setup the review analysis tab"""
        analyzer_frame = ttk.Frame(self.notebook)
        self.notebook.add(analyzer_frame, text="Analyze Reviews")

        # Title
        title_label = ttk.Label(analyzer_frame, text="Review Keyword & Time Filter", style='Title.TLabel')
        title_label.pack(pady=(10, 20))

        # Input frame
        filter_frame = ttk.LabelFrame(analyzer_frame, text="Filter Parameters", padding="15")
        filter_frame.pack(fill='x', padx=20, pady=10)

        # Load CSV button
        load_frame = ttk.Frame(filter_frame)
        load_frame.pack(fill='x', pady=(0, 15))

        ttk.Button(load_frame, text="Load CSV File", command=self.load_csv_file,
                style='Custom.TButton').pack(side='left')

        self.file_label = ttk.Label(load_frame, text="No file loaded", foreground='red')
        self.file_label.pack(side='left', padx=(15, 0))

        # Language filter
        lang_frame = ttk.Frame(filter_frame)
        lang_frame.pack(fill='x', pady=(0, 15))

        ttk.Label(lang_frame, text="Language Filter:", style='Header.TLabel').pack(side='left')

        self.language_var = tk.StringVar(value="all")
        lang_options = [("All Languages", "all"), ("English Only", "english"),
                    ("Arabic Only", "arabic"), ("Mixed Content", "mixed")]

        for text, value in lang_options:
            ttk.Radiobutton(lang_frame, text=text, variable=self.language_var,
                        value=value).pack(side='left', padx=(10, 0))

        # Keyword input
        ttk.Label(filter_frame, text="Keyword to Search:", style='Header.TLabel').pack(anchor='w', pady=(15, 5))
        self.keyword_entry = ttk.Entry(filter_frame, font=('Arial', 11), width=40)
        self.keyword_entry.pack(anchor='w', pady=(0, 15))

        # Time period frame
        time_frame = ttk.Frame(filter_frame)
        time_frame.pack(fill='x', pady=(0, 15))

        ttk.Label(time_frame, text="Time Period (days from today):", style='Header.TLabel').pack(side='left')
        self.days_var = tk.StringVar(value="30")
        self.days_spinbox = ttk.Spinbox(time_frame, from_=1, to=365, textvariable=self.days_var, width=10)
        self.days_spinbox.pack(side='left', padx=(10, 0))

        # Max results
        max_frame = ttk.Frame(filter_frame)
        max_frame.pack(fill='x', pady=(0, 15))

        ttk.Label(max_frame, text="Max Results:", style='Header.TLabel').pack(side='left')
        self.max_results_var = tk.StringVar(value="100")
        self.max_results_spinbox = ttk.Spinbox(max_frame, from_=1, to=1000, textvariable=self.max_results_var, width=10)
        self.max_results_spinbox.pack(side='left', padx=(10, 0))

        # Search button
        self.search_button = ttk.Button(filter_frame, text="Search Reviews",
                                    command=self.search_reviews, style='Custom.TButton')
        self.search_button.pack(pady=(10, 0))

        # Results frame
        results_frame = ttk.LabelFrame(analyzer_frame, text="Search Results", padding="15")
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Results summary
        self.results_label = ttk.Label(results_frame, text="Load a CSV file and enter search criteria",
                                     style='Header.TLabel')
        self.results_label.pack(pady=(0, 10))

        # Results text display
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80,
                                                     font=('Arial', 9), wrap=tk.WORD)
        self.results_text.pack(fill='both', expand=True, pady=(0, 10))

        # Export button frame
        export_frame = ttk.Frame(results_frame)
        export_frame.pack(fill='x')

        ttk.Button(export_frame, text="Export Filtered Results (CSV)",
                command=self.export_filtered_results, style='Custom.TButton').pack(side='left')

    def start_scraping(self):
        """Start the scraping process in a separate thread"""
        if not SCRAPER_AVAILABLE:
            messagebox.showerror("Error", "Scraper functions not available. Make sure google_maps_scraper.py is in the same directory.")
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a Google Maps URL")
            return

        try:
            num_reviews = int(self.num_reviews_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of reviews")
            return

        # Disable button and start progress
        self.scrape_button.config(state='disabled')
        self.progress_bar.start()
        self.progress_var.set("Scraping reviews...")

        # Start scraping in separate thread
        scraping_thread = threading.Thread(target=self.scrape_worker, args=(url, num_reviews))
        scraping_thread.daemon = True
        scraping_thread.start()

    def scrape_worker(self, url, num_reviews):
        """Worker function for scraping"""
        try:
            # Scrape reviews
            self.root.after(0, lambda: self.progress_var.set("Scraping reviews..."))
            reviews = scrape_reviews_function(url, num_reviews)

            if reviews:
                # Process reviews
                self.root.after(0, lambda: self.progress_var.set("Processing reviews..."))
                processed_reviews = process_reviews_function(reviews)

                # Store results
                self.all_reviews = processed_reviews

                # Update GUI
                self.root.after(0, self.update_scraped_results)
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No reviews were scraped. Please check the URL."))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Scraping failed: {str(e)}"))

        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.scraping_finished)

    def scraping_finished(self):
        """Clean up after scraping"""
        self.scrape_button.config(state='normal')
        self.progress_bar.stop()
        self.progress_var.set("Scraping completed!")

    def update_scraped_results(self):
        """Update the scraped results display"""
        self.scraped_text.delete(1.0, tk.END)

        if self.all_reviews:
            result_text = f"Successfully scraped {len(self.all_reviews)} reviews:\n"
            result_text += "=" * 50 + "\n\n"

            for i, review in enumerate(self.all_reviews[:5], 1):  # Show first 5
                result_text += f"Review {i}:\n"
                result_text += f"Name: {review.get('name', 'N/A')}\n"
                result_text += f"Date: {review.get('date', 'N/A')}\n"
                result_text += f"Rating: {review.get('rating', 'N/A')}\n"
                result_text += f"Text: {review.get('text', 'N/A')[:200]}{'...' if len(review.get('text', '')) > 200 else ''}\n"
                result_text += "-" * 50 + "\n\n"

            if len(self.all_reviews) > 5:
                result_text += f"... and {len(self.all_reviews) - 5} more reviews"

            self.scraped_text.insert(1.0, result_text)

    def use_for_analysis(self):
        """Use scraped reviews for analysis"""
        if not self.all_reviews:
            messagebox.showerror("Error", "No reviews available")
            return

        # Convert to DataFrame
        self.reviews_df = pd.DataFrame(self.all_reviews)
        self.file_label.config(text=f"{len(self.all_reviews)} reviews loaded from scraper", foreground='green')

        # Switch to analysis tab
        self.notebook.select(1)
        messagebox.showinfo("Success", f"Loaded {len(self.all_reviews)} reviews for analysis")

    def load_csv_file(self):
        """Load reviews from a CSV file for analysis"""
        filename = filedialog.askopenfilename(
            title="Select a CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filename:
            return

        try:
            self.reviews_df = pd.read_csv(filename)

            # Basic validation: check for a 'text' or 'date' column
            if 'text' not in self.reviews_df.columns or 'date' not in self.reviews_df.columns:
                 messagebox.showwarning("Warning", "The CSV file may not be in the correct format. Missing 'text' or 'date' columns.")

            num_reviews = len(self.reviews_df)
            self.file_label.config(text=f"{num_reviews} reviews loaded from {os.path.basename(filename)}", foreground='green')
            messagebox.showinfo("Success", f"Successfully loaded {num_reviews} reviews.")

            # Clear previous search results
            self.results_text.config(state='normal')
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, "CSV file loaded. Enter search criteria and click 'Search Reviews'.")
            self.results_text.config(state='disabled')
            self.results_label.config(text="Ready to search")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load or read CSV file:\n{e}")
            self.file_label.config(text="Failed to load file", foreground='red')

    def save_scraped_reviews(self):
        """Save scraped reviews to CSV"""
        if not self.all_reviews:
            messagebox.showerror("Error", "No reviews to save")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Reviews As"
        )

        if filename:
            try:
                scraped_df = pd.DataFrame(self.all_reviews)
                scraped_df.to_csv(filename, index=False, encoding='utf-8-sig')
                messagebox.showinfo("Success", f"Reviews saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save reviews: {str(e)}")

    def parse_date(self, date_str):
        """Parse date string to datetime object with proper debugging"""
        if not date_str or date_str == 'N/A':
            return None

        try:
            original_date_str = date_str
            date_str = date_str.strip().lower()

            if 'ago' in date_str:
                now = datetime.now()

                if 'minute' in date_str:
                    minutes = re.findall(r'(\d+)\s*minute', date_str)
                    if minutes:
                        return now - timedelta(minutes=int(minutes[0]))

                elif 'hour' in date_str:
                    hours = re.findall(r'(\d+)\s*hour', date_str)
                    if hours:
                        return now - timedelta(hours=int(hours[0]))

                elif 'day' in date_str and 'week' not in date_str:
                    days = re.findall(r'(\d+)\s*day', date_str)
                    if days:
                        return now - timedelta(days=int(days[0]))
                    elif 'a day ago' in date_str:
                        return now - timedelta(days=1)

                elif 'week' in date_str:
                    weeks = re.findall(r'(\d+)\s*week', date_str)
                    if weeks:
                        return now - timedelta(weeks=int(weeks[0]))
                    elif 'a week ago' in date_str:
                        return now - timedelta(weeks=1)

                elif 'month' in date_str:
                    months = re.findall(r'(\d+)\s*month', date_str)
                    if months:
                        return now - timedelta(days=int(months[0])*30)
                    elif 'a month ago' in date_str:
                        return now - timedelta(days=30)

            date_formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%d-%m-%Y',
                '%B %d, %Y',
                '%b %d, %Y',
            ]

            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except ValueError:
                    continue

            return None

        except Exception:
            return None

    def search_reviews(self):
        """Search reviews based on keyword and time period with proper date filtering"""
        if self.reviews_df is None:
            messagebox.showerror("Error", "Please load a CSV file first")
            return

        keyword_input = self.keyword_entry.get().strip()
        keywords = [k.strip() for k in keyword_input.split(',') if k.strip()]

        if not keywords and keyword_input:
            messagebox.showerror("Error", "Please enter a keyword to search, or leave blank to skip keyword filtering.")
            return

        try:
            days = int(self.days_var.get())
            max_results = int(self.max_results_var.get())
            language_filter = self.language_var.get()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for days and max results")
            return

        cutoff_date = datetime.now() - timedelta(days=days)

        filtered_df = self.reviews_df.copy()

        # Step 1: Filter by time period
        date_filtered = []
        for _, row in filtered_df.iterrows():
            review_date = self.parse_date(row['date'])
            if review_date is None:
                continue
            if review_date >= cutoff_date:
                date_filtered.append(row)

        date_filtered_df = pd.DataFrame(date_filtered)

        # Apply keyword filtering if keywords are provided
        if keywords:
            keyword_condition = False
            for kw in keywords:
                kw_lower = kw.lower()
                keyword_condition |= (date_filtered_df['text'].str.lower().str.contains(kw_lower, na=False) |
                                      date_filtered_df['name'].str.lower().str.contains(kw_lower, na=False))
            filtered_df = date_filtered_df[keyword_condition]
        else:
            filtered_df = date_filtered_df.copy()

        # Step 3: Filter by language
        if language_filter != "all":
            language_filtered = []
            for review in filtered_df.to_dict('records'):
                detected_lang = detect_review_language(str(review.get('text', '')))
                if ((language_filter == "english" and detected_lang == "english") or
                    (language_filter == "arabic" and detected_lang == "arabic") or
                    (language_filter == "mixed" and detected_lang == "mixed")):
                    language_filtered.append(review)
            filtered_df = pd.DataFrame(language_filtered)

        # Step 4: Limit results
        self.filtered_reviews = filtered_df.head(max_results).to_dict('records')

        # Display results
        self.display_search_results(keyword_input, days, language_filter)

    def display_search_results(self, keyword_input, days, language_filter):
        """Display search results in the text widget"""
        self.results_text.delete(1.0, tk.END)

        lang_desc = {
            "all": "all languages",
            "english": "English only",
            "arabic": "Arabic only",
            "mixed": "mixed content"
        }.get(language_filter, language_filter)

        if not self.filtered_reviews:
            result_text = f"No reviews found containing '{keyword_input}' in {lang_desc} from the last {days} days.\n"
            self.results_label.config(text="No results found")
        else:
            result_text = f"Found {len(self.filtered_reviews)} reviews containing '{keyword_input}' in {lang_desc} from the last {days} days:\n"
            result_text += "=" * 80 + "\n\n"

            for i, review in enumerate(self.filtered_reviews, 1):
                review_text = review.get('text', 'N/A')
                title_text = review.get('name', 'N/A')
                detected_lang = detect_review_language(review_text)

                result_text += f"Review {i}: [{detected_lang.upper()}]\n"
                result_text += f"Name: {title_text}\n"
                result_text += f"Date: {review.get('date', 'N/A')}\n"
                result_text += f"Rating: {review.get('rating', 'N/A')}\n"
                result_text += f"Review: {review_text}\n\n"

            self.results_label.config(text=f"{len(self.filtered_reviews)} results found")

        self.results_text.config(state='normal')
        self.results_text.insert(1.0, result_text)
        self.results_text.config(state='disabled')

    def export_filtered_results(self):
        """Export filtered results to CSV"""
        if not self.filtered_reviews:
            messagebox.showerror("Error", "No filtered results to export")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Filtered Results As"
        )

        if filename:
            try:
                filtered_df = pd.DataFrame(self.filtered_reviews)
                filtered_df.to_csv(filename, index=False, encoding='utf-8-sig')
                messagebox.showinfo("Success", f"Filtered results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")


def main():
    root = tk.Tk()
    app = ReviewAnalyzerGUI(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
