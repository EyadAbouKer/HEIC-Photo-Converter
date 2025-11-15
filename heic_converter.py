import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
import threading

# Register HEIF opener with Pillow
register_heif_opener()


class HEICConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to PNG Converter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="HEIC to PNG Converter", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Convert HEIC images to PNG format",
            font=("Arial", 10)
        )
        desc_label.pack(pady=(0, 30))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        # Convert folder button
        self.folder_btn = ttk.Button(
            buttons_frame,
            text="📁 Convert Folder",
            command=self.convert_folder,
            width=25
        )
        self.folder_btn.pack(pady=10)
        
        # Convert files button
        self.files_btn = ttk.Button(
            buttons_frame,
            text="🖼️ Convert Selected Files",
            command=self.convert_files,
            width=25
        )
        self.files_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            font=("Arial", 9),
            foreground="gray"
        )
        self.status_label.pack(pady=10)
        
        # Results text area
        self.results_text = tk.Text(
            main_frame,
            height=8,
            width=70,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.pack(pady=(10, 0))
        
    def update_status(self, message, color="gray"):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)
        self.root.update_idletasks()
        
    def add_result(self, message):
        """Add message to results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
        
    def clear_results(self):
        """Clear results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
    def convert_heic_to_png(self, heic_path, output_path=None):
        """Convert a single HEIC file to PNG"""
        try:
            if output_path is None:
                output_path = heic_path.rsplit('.', 1)[0] + '.png'
            
            # Open and convert
            image = Image.open(heic_path)
            image.save(output_path, "PNG")
            
            return True, output_path
        except Exception as e:
            return False, str(e)
            
    def convert_folder(self):
        """Convert all HEIC files in a selected folder"""
        folder_path = filedialog.askdirectory(title="Select Folder with HEIC Images")
        
        if not folder_path:
            return
            
        # Run conversion in a separate thread to keep UI responsive
        thread = threading.Thread(
            target=self._convert_folder_thread,
            args=(folder_path,),
            daemon=True
        )
        thread.start()
        
    def _convert_folder_thread(self, folder_path):
        """Thread worker for folder conversion"""
        # Disable buttons during conversion
        self.folder_btn.config(state=tk.DISABLED)
        self.files_btn.config(state=tk.DISABLED)
        
        self.clear_results()
        self.progress.start(10)
        self.update_status("Scanning folder...", "blue")
        
        # Find all HEIC files
        heic_files = []
        for ext in ['*.heic', '*.HEIC', '*.heif', '*.HEIF']:
            heic_files.extend(Path(folder_path).glob(ext))
            
        if not heic_files:
            self.progress.stop()
            self.update_status("No HEIC files found", "orange")
            self.add_result("No HEIC files found in the selected folder.")
            self.folder_btn.config(state=tk.NORMAL)
            self.files_btn.config(state=tk.NORMAL)
            return
            
        self.add_result(f"Found {len(heic_files)} HEIC file(s) to convert:\n")
        
        # Convert each file
        success_count = 0
        fail_count = 0
        
        for heic_file in heic_files:
            filename = heic_file.name
            self.update_status(f"Converting {filename}...", "blue")
            
            success, result = self.convert_heic_to_png(str(heic_file))
            
            if success:
                success_count += 1
                self.add_result(f"✓ {filename} → {Path(result).name}")
            else:
                fail_count += 1
                self.add_result(f"✗ {filename} - Error: {result}")
                
        # Show completion message
        self.progress.stop()
        
        summary = f"\n{'='*50}\n"
        summary += f"Conversion complete!\n"
        summary += f"Success: {success_count} | Failed: {fail_count}\n"
        summary += f"{'='*50}"
        self.add_result(summary)
        
        if fail_count == 0:
            self.update_status("All files converted successfully!", "green")
            messagebox.showinfo(
                "Success",
                f"Successfully converted {success_count} file(s) to PNG!"
            )
        else:
            self.update_status("Conversion completed with errors", "orange")
            messagebox.showwarning(
                "Completed with Errors",
                f"Converted {success_count} file(s).\n{fail_count} file(s) failed."
            )
            
        # Re-enable buttons
        self.folder_btn.config(state=tk.NORMAL)
        self.files_btn.config(state=tk.NORMAL)
        
    def convert_files(self):
        """Convert selected HEIC files"""
        file_paths = filedialog.askopenfilenames(
            title="Select HEIC Images",
            filetypes=[
                ("HEIC files", "*.heic *.HEIC *.heif *.HEIF"),
                ("All files", "*.*")
            ]
        )
        
        if not file_paths:
            return
            
        # Run conversion in a separate thread
        thread = threading.Thread(
            target=self._convert_files_thread,
            args=(file_paths,),
            daemon=True
        )
        thread.start()
        
    def _convert_files_thread(self, file_paths):
        """Thread worker for file conversion"""
        # Disable buttons during conversion
        self.folder_btn.config(state=tk.DISABLED)
        self.files_btn.config(state=tk.DISABLED)
        
        self.clear_results()
        self.progress.start(10)
        self.update_status("Converting files...", "blue")
        
        self.add_result(f"Converting {len(file_paths)} file(s):\n")
        
        # Convert each file
        success_count = 0
        fail_count = 0
        
        for file_path in file_paths:
            filename = Path(file_path).name
            self.update_status(f"Converting {filename}...", "blue")
            
            success, result = self.convert_heic_to_png(file_path)
            
            if success:
                success_count += 1
                self.add_result(f"✓ {filename} → {Path(result).name}")
            else:
                fail_count += 1
                self.add_result(f"✗ {filename} - Error: {result}")
                
        # Show completion message
        self.progress.stop()
        
        summary = f"\n{'='*50}\n"
        summary += f"Conversion complete!\n"
        summary += f"Success: {success_count} | Failed: {fail_count}\n"
        summary += f"{'='*50}"
        self.add_result(summary)
        
        if fail_count == 0:
            self.update_status("All files converted successfully!", "green")
            messagebox.showinfo(
                "Success",
                f"Successfully converted {success_count} file(s) to PNG!"
            )
        else:
            self.update_status("Conversion completed with errors", "orange")
            messagebox.showwarning(
                "Completed with Errors",
                f"Converted {success_count} file(s).\n{fail_count} file(s) failed."
            )
            
        # Re-enable buttons
        self.folder_btn.config(state=tk.NORMAL)
        self.files_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = HEICConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

