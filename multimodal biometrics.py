import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
import os
import json
from PIL import Image, ImageTk


class BiometricSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Biometric Identification System")
        self.root.geometry("800x600")
        
        self.db_file = "biometric_database.json"
        self.biometric_db = self.load_database()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
       
        self.fingerprint_enrollment_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fingerprint_enrollment_tab, text="Fingerprint Enrollment")
        self.setup_fingerprint_enrollment_tab()
        
        self.iris_enrollment_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.iris_enrollment_tab, text="Iris Enrollment")
        self.setup_iris_enrollment_tab()
        
        self.fingerprint_verification_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fingerprint_verification_tab, text="Fingerprint Verification")
        self.setup_fingerprint_verification_tab()
        
        self.iris_verification_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.iris_verification_tab, text="Iris Verification")
        self.setup_iris_verification_tab()
    
    def load_database(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as file:
                    return json.load(file)
            except:
                return {}
        else:
            return {}
    
    def save_database(self):
        with open(self.db_file, 'w') as file:
            json.dump(self.biometric_db, file)
    
    def setup_fingerprint_enrollment_tab(self):
        
        form_frame = ttk.LabelFrame(self.fingerprint_enrollment_tab, text="User Information")
        form_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.fp_id_entry = ttk.Entry(form_frame)
        self.fp_id_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.fp_name_entry = ttk.Entry(form_frame)
        self.fp_name_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.fp_gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(form_frame, textvariable=self.fp_gender_var)
        gender_combo['values'] = ('Male', 'Female', 'Other')
        gender_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Age:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.fp_age_entry = ttk.Entry(form_frame)
        self.fp_age_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
       
        fp_frame = ttk.LabelFrame(self.fingerprint_enrollment_tab, text="Fingerprint")
        fp_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)
        
        self.fp_enrollment_image_label = ttk.Label(fp_frame)
        self.fp_enrollment_image_label.pack(fill='both', expand=True, padx=10, pady=10)
       
        self.fp_upload_btn = ttk.Button(fp_frame, text="Upload Fingerprint", command=self.upload_fingerprint)
        self.fp_upload_btn.pack(padx=10, pady=10)
        
        self.fp_enroll_btn = ttk.Button(fp_frame, text="Enroll User", command=self.enroll_fingerprint_user)
        self.fp_enroll_btn.pack(padx=10, pady=10)
        
        self.enrollment_fingerprint = None
        self.fp_enrollment_image = None
    
    def setup_iris_enrollment_tab(self):
        
        form_frame = ttk.LabelFrame(self.iris_enrollment_tab, text="User Information")
        form_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.iris_id_entry = ttk.Entry(form_frame)
        self.iris_id_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.iris_name_entry = ttk.Entry(form_frame)
        self.iris_name_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
      
        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.iris_gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(form_frame, textvariable=self.iris_gender_var)
        gender_combo['values'] = ('Male', 'Female', 'Other')
        gender_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Age:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.iris_age_entry = ttk.Entry(form_frame)
        self.iris_age_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
    
        ttk.Label(form_frame, text="Eye:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.iris_eye_var = tk.StringVar()
        eye_combo = ttk.Combobox(form_frame, textvariable=self.iris_eye_var)
        eye_combo['values'] = ('Left Eye', 'Right Eye', 'Both Eyes')
        eye_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        iris_frame = ttk.LabelFrame(self.iris_enrollment_tab, text="Iris Image")
        iris_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)
        
        self.iris_enrollment_image_label = ttk.Label(iris_frame)
        self.iris_enrollment_image_label.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.iris_upload_btn = ttk.Button(iris_frame, text="Upload Iris Image", command=self.upload_iris)
        self.iris_upload_btn.pack(padx=10, pady=10)
       
        self.iris_enroll_btn = ttk.Button(iris_frame, text="Enroll User", command=self.enroll_iris_user)
        self.iris_enroll_btn.pack(padx=10, pady=10)
        
        self.enrollment_iris = None
        self.iris_enrollment_image = None
    
    def setup_fingerprint_verification_tab(self):
        
        verify_frame = ttk.LabelFrame(self.fingerprint_verification_tab, text="Verify Fingerprint")
        verify_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
      
        self.fp_verification_image_label = ttk.Label(verify_frame)
        self.fp_verification_image_label.pack(fill='both', expand=True, padx=10, pady=10)
     
        self.fp_verify_upload_btn = ttk.Button(verify_frame, text="Upload Fingerprint", command=self.upload_verification_fingerprint)
        self.fp_verify_upload_btn.pack(padx=10, pady=10)
      
        self.fp_verify_btn = ttk.Button(verify_frame, text="Verify Identity", command=self.verify_fingerprint)
        self.fp_verify_btn.pack(padx=10, pady=10)
   
        results_frame = ttk.LabelFrame(self.fingerprint_verification_tab, text="Results")
        results_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)
        
        self.fp_result_text = tk.Text(results_frame, height=20, width=40)
        self.fp_result_text.pack(fill='both', expand=True, padx=10, pady=10)
       
        self.verification_fingerprint = None
        self.fp_verification_image = None
    
    def setup_iris_verification_tab(self):
     
        verify_frame = ttk.LabelFrame(self.iris_verification_tab, text="Verify Iris")
        verify_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        
        self.iris_verification_image_label = ttk.Label(verify_frame)
        self.iris_verification_image_label.pack(fill='both', expand=True, padx=10, pady=10)
       
        self.iris_verify_upload_btn = ttk.Button(verify_frame, text="Upload Iris Image", command=self.upload_verification_iris)
        self.iris_verify_upload_btn.pack(padx=10, pady=10)
        
        self.iris_verify_btn = ttk.Button(verify_frame, text="Verify Identity", command=self.verify_iris)
        self.iris_verify_btn.pack(padx=10, pady=10)
      
        results_frame = ttk.LabelFrame(self.iris_verification_tab, text="Results")
        results_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)
       
        self.iris_result_text = tk.Text(results_frame, height=20, width=40)
        self.iris_result_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.verification_iris = None
        self.iris_verification_image = None
    
    def upload_fingerprint(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            try:
                
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            
                self.enrollment_fingerprint = self.process_fingerprint(img)
               
                self.fp_enrollment_image = Image.open(file_path)
                self.fp_enrollment_image = self.fp_enrollment_image.resize((200, 200))
                img_tk = ImageTk.PhotoImage(self.fp_enrollment_image)
                self.fp_enrollment_image_label.configure(image=img_tk)
                self.fp_enrollment_image_label.image = img_tk
                
                messagebox.showinfo("Success", "Fingerprint uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load fingerprint: {str(e)}")
    
    def upload_iris(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            try:
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
              
                self.enrollment_iris = self.process_iris(img)
                
                self.iris_enrollment_image = Image.open(file_path)
                self.iris_enrollment_image = self.iris_enrollment_image.resize((200, 200))
                img_tk = ImageTk.PhotoImage(self.iris_enrollment_image)
                self.iris_enrollment_image_label.configure(image=img_tk)
                self.iris_enrollment_image_label.image = img_tk
                
                messagebox.showinfo("Success", "Iris image uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load iris image: {str(e)}")
    
    def upload_verification_fingerprint(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            try:
                
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                
                self.verification_fingerprint = self.process_fingerprint(img)
                
                self.fp_verification_image = Image.open(file_path)
                self.fp_verification_image = self.fp_verification_image.resize((200, 200))
                img_tk = ImageTk.PhotoImage(self.fp_verification_image)
                self.fp_verification_image_label.configure(image=img_tk)
                self.fp_verification_image_label.image = img_tk
                
                messagebox.showinfo("Success", "Fingerprint uploaded for verification!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load fingerprint: {str(e)}")
    
    def upload_verification_iris(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            try:
                
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                
                self.verification_iris = self.process_iris(img)
                
                self.iris_verification_image = Image.open(file_path)
                self.iris_verification_image = self.iris_verification_image.resize((200, 200))
                img_tk = ImageTk.PhotoImage(self.iris_verification_image)
                self.iris_verification_image_label.configure(image=img_tk)
                self.iris_verification_image_label.image = img_tk
                
                messagebox.showinfo("Success", "Iris image uploaded for verification!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load iris image: {str(e)}")
    
    def process_fingerprint(self, img):
        """
        Process fingerprint image to extract features for matching
        """
    
        img = cv2.resize(img, (200, 200))
        
        img = cv2.equalizeHist(img)
        
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
       
        orb = cv2.ORB_create()
        keypoints, descriptors = orb.detectAndCompute(thresh, None)
        
        # Convert descriptors to list for JSON storage
        if descriptors is not None:
            descriptors_list = descriptors.tolist()
        else:
            descriptors_list = []
            
        return {
            "descriptors": descriptors_list,
            "hash": hash(str(descriptors_list))  
        }
    
    def process_iris(self, img):
        """
        Process iris image to extract features for matching
        """
        
        img = cv2.resize(img, (200, 200))
        
        img = cv2.equalizeHist(img)
        
        img = cv2.GaussianBlur(img, (5, 5), 0)
        
        circles = cv2.HoughCircles(
            img, 
            cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=50, 
            param1=50, 
            param2=30, 
            minRadius=20, 
            maxRadius=100
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                
                mask = np.zeros_like(img)
                cv2.circle(mask, (i[0], i[1]), i[2], 255, -1)
                img = cv2.bitwise_and(img, mask)
     
        orb = cv2.ORB_create(nfeatures=1000)
        keypoints, descriptors = orb.detectAndCompute(img, None)
        
      
        if descriptors is not None:
            descriptors_list = descriptors.tolist()
        else:
            descriptors_list = []
            
        return {
            "descriptors": descriptors_list,
            "hash": hash(str(descriptors_list))  
        }
    
    def enroll_fingerprint_user(self):
       
        if not self.enrollment_fingerprint:
            messagebox.showerror("Error", "Please upload a fingerprint image first!")
            return
        
        user_id = self.fp_id_entry.get().strip()
        name = self.fp_name_entry.get().strip()
        gender = self.fp_gender_var.get()
        age = self.fp_age_entry.get().strip()
        
        if not user_id or not name or not gender or not age:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            age = int(age)
            if age <= 0:
                messagebox.showerror("Error", "Age must be a positive number!")
                return
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return
       
        if user_id not in self.biometric_db:
            self.biometric_db[user_id] = {
                "id": user_id,
                "name": name,
                "gender": gender,
                "age": age,
                "fingerprint": self.enrollment_fingerprint,
                "iris": None
            }
        else:
            
            self.biometric_db[user_id]["name"] = name
            self.biometric_db[user_id]["gender"] = gender
            self.biometric_db[user_id]["age"] = age
            self.biometric_db[user_id]["fingerprint"] = self.enrollment_fingerprint
       
        self.save_database()
        
        self.fp_id_entry.delete(0, tk.END)
        self.fp_name_entry.delete(0, tk.END)
        self.fp_gender_var.set('')
        self.fp_age_entry.delete(0, tk.END)
        self.fp_enrollment_image_label.configure(image='')
        self.enrollment_fingerprint = None
        
        messagebox.showinfo("Success", f"User {name} has been enrolled with fingerprint successfully!")
    
    def enroll_iris_user(self):
        
        if not self.enrollment_iris:
            messagebox.showerror("Error", "Please upload an iris image first!")
            return
        
        user_id = self.iris_id_entry.get().strip()
        name = self.iris_name_entry.get().strip()
        gender = self.iris_gender_var.get()
        age = self.iris_age_entry.get().strip()
        eye = self.iris_eye_var.get()
        
        if not user_id or not name or not gender or not age or not eye:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            age = int(age)
            if age <= 0:
                messagebox.showerror("Error", "Age must be a positive number!")
                return
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return
        
        if user_id not in self.biometric_db:
            self.biometric_db[user_id] = {
                "id": user_id,
                "name": name,
                "gender": gender,
                "age": age,
                "fingerprint": None,
                "iris": {
                    "data": self.enrollment_iris,
                    "eye": eye
                }
            }
        else:
           
            self.biometric_db[user_id]["name"] = name
            self.biometric_db[user_id]["gender"] = gender
            self.biometric_db[user_id]["age"] = age
            self.biometric_db[user_id]["iris"] = {
                "data": self.enrollment_iris,
                "eye": eye
            }
        
        self.save_database()
        
        self.iris_id_entry.delete(0, tk.END)
        self.iris_name_entry.delete(0, tk.END)
        self.iris_gender_var.set('')
        self.iris_age_entry.delete(0, tk.END)
        self.iris_eye_var.set('')
        self.iris_enrollment_image_label.configure(image='')
        self.enrollment_iris = None
        
        messagebox.showinfo("Success", f"User {name} has been enrolled with iris successfully!")
    
    def verify_fingerprint(self):
        if not self.verification_fingerprint:
            messagebox.showerror("Error", "Please upload a fingerprint image first!")
            return
        
        self.fp_result_text.delete(1.0, tk.END)
        
        has_fingerprints = False
        for user_data in self.biometric_db.values():
            if user_data["fingerprint"] is not None:
                has_fingerprints = True
                break
                
        if not has_fingerprints:
            self.fp_result_text.insert(tk.END, "No fingerprints in database. Please enroll users first.")
            return
        
        best_match = None
        best_score = 0
        
        for user_id, user_data in self.biometric_db.items():
            if user_data["fingerprint"] is not None:
                score = self.match_fingerprints(self.verification_fingerprint, user_data["fingerprint"])
                if score > best_score:
                    best_score = score
                    best_match = user_data
       
        if best_score > 60:  
            self.fp_result_text.insert(tk.END, "✓ MATCH FOUND\n\n")
            self.fp_result_text.insert(tk.END, f"ID: {best_match['id']}\n")
            self.fp_result_text.insert(tk.END, f"Name: {best_match['name']}\n")
            self.fp_result_text.insert(tk.END, f"Gender: {best_match['gender']}\n")
            self.fp_result_text.insert(tk.END, f"Age: {best_match['age']}\n\n")
            self.fp_result_text.insert(tk.END, f"Match Accuracy: {best_score:.2f}%")
        else:
            self.fp_result_text.insert(tk.END, "✗ NO MATCH FOUND\n\n")
            self.fp_result_text.insert(tk.END, f"Best match score: {best_score:.2f}%\n")
            self.fp_result_text.insert(tk.END, "The fingerprint does not match any enrolled user.")
    
    def verify_iris(self):
        if not self.verification_iris:
            messagebox.showerror("Error", "Please upload an iris image first!")
            return
        
        self.iris_result_text.delete(1.0, tk.END)
        
        has_iris = False
        for user_data in self.biometric_db.values():
            if user_data["iris"] is not None:
                has_iris = True
                break
                
        if not has_iris:
            self.iris_result_text.insert(tk.END, "No iris data in database. Please enroll users first.")
            return
        
        best_match = None
        best_score = 0
        
        for user_id, user_data in self.biometric_db.items():
            if user_data["iris"] is not None:
                score = self.match_iris(self.verification_iris, user_data["iris"]["data"])
                if score > best_score:
                    best_score = score
                    best_match = user_data
        
        if best_score > 60:  
            self.iris_result_text.insert(tk.END, "✓ MATCH FOUND\n\n")
            self.iris_result_text.insert(tk.END, f"ID: {best_match['id']}\n")
            self.iris_result_text.insert(tk.END, f"Name: {best_match['name']}\n")
            self.iris_result_text.insert(tk.END, f"Gender: {best_match['gender']}\n")
            self.iris_result_text.insert(tk.END, f"Age: {best_match['age']}\n")
            if best_match["iris"] is not None:
                self.iris_result_text.insert(tk.END, f"Eye: {best_match['iris']['eye']}\n\n")
            self.iris_result_text.insert(tk.END, f"Match Accuracy: {best_score:.2f}%")
        else:
            self.iris_result_text.insert(tk.END, "✗ NO MATCH FOUND\n\n")
            self.iris_result_text.insert(tk.END, f"Best match score: {best_score:.2f}%\n")
            self.iris_result_text.insert(tk.END, "The iris does not match any enrolled user.")
    
    def match_fingerprints(self, fp1, fp2):
        """
        Compare two fingerprints and return a match score (0-100)
        """
        
        if fp1["hash"] == fp2["hash"]:
            return 100.0
        
        desc1 = np.array(fp1["descriptors"])
        desc2 = np.array(fp2["descriptors"])
        
        if len(desc1) == 0 or len(desc2) == 0:
            return 0.0
        
        try:
            
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
           
            matches = bf.match(desc1, desc2)
            
            max_matches = min(len(desc1), len(desc2))
            if max_matches == 0:
                return 0.0
                
            score = (len(matches) / max_matches) * 100
            
            return min(score, 100.0)
        except Exception:
            
            return 0.0
    
    def match_iris(self, iris1, iris2):
        """
        Compare two iris data and return a match score (0-100)
        """
        if iris1["hash"] == iris2["hash"]:
            return 100.0
        
        desc1 = np.array(iris1["descriptors"])
        desc2 = np.array(iris2["descriptors"])
        
        if len(desc1) == 0 or len(desc2) == 0:
            return 0.0
        
        try:
            
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            
            matches = bf.match(desc1, desc2)
            max_matches = min(len(desc1), len(desc2))
            if max_matches == 0:
                return 0.0
                
            score = (len(matches) / max_matches) * 100
            
            score = min(score * 1.1, 100.0)
            
            return score
        except Exception:
            
            return 0.0
        
def main():
    root = tk.Tk()
    app = BiometricSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()