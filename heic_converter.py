import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

# Register HEIF opener with Pillow
register_heif_opener()


class HEICConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC Image Converter")
        self.root.geometry("600x450")
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
            text="HEIC Image Converter", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Convert HEIC images to PNG or JPEG format",
            font=("Arial", 10)
        )
        desc_label.pack(pady=(0, 20))
        
        # Output format selection frame
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(pady=10)
        
        format_label = ttk.Label(
            format_frame,
            text="Output Format:",
            font=("Arial", 10, "bold")
        )
        format_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Output format variable (default to JPEG)
        self.output_format = tk.StringVar(value="JPEG")
        
        # Radio buttons for format selection
        jpeg_radio = ttk.Radiobutton(
            format_frame,
            text="JPEG",
            variable=self.output_format,
            value="JPEG"
        )
        jpeg_radio.pack(side=tk.LEFT, padx=5)
        
        png_radio = ttk.Radiobutton(
            format_frame,
            text="PNG",
            variable=self.output_format,
            value="PNG"
        )
        png_radio.pack(side=tk.LEFT, padx=5)
        
        # Quality setting for JPEG (only visible when JPEG is selected)
        self.quality_frame = ttk.Frame(main_frame)
        
        quality_label = ttk.Label(
            self.quality_frame,
            text="JPEG Quality:",
            font=("Arial", 9)
        )
        quality_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.quality_var = tk.IntVar(value=95)
        quality_slider = ttk.Scale(
            self.quality_frame,
            from_=50,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            length=150
        )
        quality_slider.pack(side=tk.LEFT, padx=5)
        
        self.quality_value_label = ttk.Label(
            self.quality_frame,
            text="95",
            font=("Arial", 9, "bold")
        )
        self.quality_value_label.pack(side=tk.LEFT, padx=5)
        
        # Update quality label when slider moves
        quality_slider.config(command=lambda v: self.quality_value_label.config(text=str(int(float(v)))))
        
        # Show quality frame by default (JPEG is default)
        self.quality_frame.pack(pady=5)
        
        # Bind format change to show/hide quality slider
        self.output_format.trace_add('write', self.on_format_change)
        
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
    
    def on_format_change(self, *args):
        """Show/hide JPEG quality slider based on selected format"""
        if self.output_format.get() == "JPEG":
            self.quality_frame.pack(pady=5)
        else:
            self.quality_frame.pack_forget()
        
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
        
    def convert_heic_to_image(self, heic_path, output_format="PNG", quality=95, output_path=None):
        """Convert a single HEIC file to PNG or JPEG and delete the original HEIC"""
        try:
            # Determine output extension
            ext = '.png' if output_format == "PNG" else '.jpg'
            
            if output_path is None:
                output_path = heic_path.rsplit('.', 1)[0] + ext
            
            # Open and convert
            image = Image.open(heic_path)
            
            # Convert to RGB if saving as JPEG (JPEG doesn't support transparency)
            if output_format == "JPEG" and image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                image = rgb_image
            
            # Save with appropriate settings
            if output_format == "PNG":
                image.save(output_path, "PNG", optimize=True)
            else:  # JPEG
                image.save(output_path, "JPEG", quality=quality, optimize=True)
            
            # Delete the original HEIC file after successful conversion
            try:
                os.remove(heic_path)
            except Exception as e:
                return True, f"{output_path} (Warning: Could not delete original: {str(e)})"
            
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
        """Thread worker for folder conversion with parallel processing"""
        # Disable buttons during conversion
        self.folder_btn.config(state=tk.DISABLED)
        self.files_btn.config(state=tk.DISABLED)
        
        # Get selected format and quality
        output_format = self.output_format.get()
        quality = self.quality_var.get()
        
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
            
        format_text = f"{output_format}" + (f" (Quality: {quality})" if output_format == "JPEG" else "")
        self.add_result(f"Found {len(heic_files)} HEIC file(s) to convert to {format_text}:\n")
        self.add_result(f"Using parallel processing with {min(4, len(heic_files))} workers...\n")
        
        # Convert files in parallel using ThreadPoolExecutor
        success_count = 0
        fail_count = 0
        
        # Use up to 4 workers for parallel processing (good balance for most systems)
        max_workers = min(4, len(heic_files))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all conversion tasks
            future_to_file = {
                executor.submit(self.convert_heic_to_image, str(heic_file), output_format, quality): heic_file 
                for heic_file in heic_files
            }
            
            # Process results as they complete
            for future in as_completed(future_to_file):
                heic_file = future_to_file[future]
                filename = heic_file.name
                
                try:
                    success, result = future.result()
                    
                    if success:
                        success_count += 1
                        self.add_result(f"✓ {filename} → {Path(result).name}")
                    else:
                        fail_count += 1
                        self.add_result(f"✗ {filename} - Error: {result}")
                except Exception as e:
                    fail_count += 1
                    self.add_result(f"✗ {filename} - Error: {str(e)}")
                
        # Show completion message
        self.progress.stop()
        
        summary = f"\n{'='*50}\n"
        summary += f"Conversion complete!\n"
        summary += f"Success: {success_count} | Failed: {fail_count}\n"
        summary += f"Original HEIC files have been deleted.\n"
        summary += f"{'='*50}"
        self.add_result(summary)
        
        if fail_count == 0:
            self.update_status("All files converted successfully!", "green")
            messagebox.showinfo(
                "Success",
                f"Successfully converted {success_count} file(s) to {output_format}!\nOriginal HEIC files have been deleted."
            )
        else:
            self.update_status("Conversion completed with errors", "orange")
            messagebox.showwarning(
                "Completed with Errors",
                f"Converted {success_count} file(s) to {output_format}.\n{fail_count} file(s) failed.\nOriginal HEIC files were deleted for successful conversions only."
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
        """Thread worker for file conversion with parallel processing"""
        # Disable buttons during conversion
        self.folder_btn.config(state=tk.DISABLED)
        self.files_btn.config(state=tk.DISABLED)
        
        # Get selected format and quality
        output_format = self.output_format.get()
        quality = self.quality_var.get()
        
        self.clear_results()
        self.progress.start(10)
        self.update_status("Converting files...", "blue")
        
        format_text = f"{output_format}" + (f" (Quality: {quality})" if output_format == "JPEG" else "")
        self.add_result(f"Converting {len(file_paths)} file(s) to {format_text}:\n")
        self.add_result(f"Using parallel processing with {min(4, len(file_paths))} workers...\n")
        
        # Convert files in parallel using ThreadPoolExecutor
        success_count = 0
        fail_count = 0
        
        # Use up to 4 workers for parallel processing (good balance for most systems)
        max_workers = min(4, len(file_paths))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all conversion tasks
            future_to_file = {
                executor.submit(self.convert_heic_to_image, file_path, output_format, quality): file_path 
                for file_path in file_paths
            }
            
            # Process results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                filename = Path(file_path).name
                
                try:
                    success, result = future.result()
                    
                    if success:
                        success_count += 1
                        self.add_result(f"✓ {filename} → {Path(result).name}")
                    else:
                        fail_count += 1
                        self.add_result(f"✗ {filename} - Error: {result}")
                except Exception as e:
                    fail_count += 1
                    self.add_result(f"✗ {filename} - Error: {str(e)}")
                
        # Show completion message
        self.progress.stop()
        
        summary = f"\n{'='*50}\n"
        summary += f"Conversion complete!\n"
        summary += f"Success: {success_count} | Failed: {fail_count}\n"
        summary += f"Original HEIC files have been deleted.\n"
        summary += f"{'='*50}"
        self.add_result(summary)
        
        if fail_count == 0:
            self.update_status("All files converted successfully!", "green")
            messagebox.showinfo(
                "Success",
                f"Successfully converted {success_count} file(s) to {output_format}!\nOriginal HEIC files have been deleted."
            )
        else:
            self.update_status("Conversion completed with errors", "orange")
            messagebox.showwarning(
                "Completed with Errors",
                f"Converted {success_count} file(s) to {output_format}.\n{fail_count} file(s) failed.\nOriginal HEIC files were deleted for successful conversions only."
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

