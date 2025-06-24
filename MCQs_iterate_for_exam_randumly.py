import random
import tkinter as tk
from tkinter import messagebox # Explicit import for messagebox

# Your QuizGenerator class with the new questions
class QuizGenerator:
    def __init__(self):
        self.questions = [

            {
                "question": "What is a potential problem associated with anatomical contouring of denture flanges, especially when extensively stippled?",
                "options": [
                    "It reduces denture retention",
                    "It makes the denture too heavy",
                    "Difficulty in keeping the flanges clean",
                    "It compromises the strength of the acrylic"
                ],
                "correct_answer": "Difficulty in keeping the flanges clean"
            },
            {
                "question": "Which of these is NOT listed as a benefit of properly contoured dentures?",
                "options": [
                    "Improved tolerance and comfort",
                    "Facilitates stability and control",
                    "Prevents chronic biting of the lip or cheek",
                    "Significantly increases masticatory force"
                ],
                "correct_answer": "Significantly increases masticatory force"
            },
            {
                "question": "What is the primary aim of 'Characterization' in complete dentures?",
                "options": [
                    "To make all dentures look identical for easier manufacturing",
                    "To alter the denture with unique markings and colorations to enhance natural appearance",
                    "To strictly follow ideal anatomical forms without deviation",
                    "To reduce the cost of the denture prosthesis"
                ],
                "correct_answer": "To alter the denture with unique markings and colorations to enhance natural appearance"
            },
            {
                "question": "The Frush and Fisher dentogenic concept for esthetic planning includes the effects of which three main factors?",
                "options": [
                    "Material, technique, and laboratory skill",
                    "Age, sex, and personality",
                    "Occlusion, phonetics, and mastication",
                    "Impression, jaw relation, and try-in"
                ],
                "correct_answer": "Age, sex, and personality"
            },
            {
                "question": "Which of the following is a method of characterization mentioned in the PDF?",
                "options": [
                    "Using a single, uniform tooth shade for all teeth",
                    "Perfectly symmetrical tooth arrangement",
                    "Stippling, staining, and tinting of the denture base",
                    "Avoiding any form of tooth rotation or tilting"
                ],
                "correct_answer": "Stippling, staining, and tinting of the denture base"
            },
            {
                "question": "The final decision for esthetics in complete dentures depends on maxillomandibular relationships, patient's appearance, functional requirements, and what other crucial factor?",
                "options": [
                    "The dentist's preferred artistic style",
                    "The cost of the materials used",
                    "Patient's mental attitude",
                    "The type of articulator used"
                ],
                "correct_answer": "Patient's mental attitude"
            }

        ]

    # 1234
    def generate_quiz(self, num_questions=6):  # Default to the number of questions available
        # Ensure num_questions does not exceed the available questions
        actual_num_questions = min(num_questions, len(self.questions))
        if actual_num_questions == 0:
            return []  # Return empty list if no questions
        return random.sample(self.questions, actual_num_questions)

class QuizApp:
    def __init__(self, quiz_generator):
        self.quiz_generator = quiz_generator
        self.quiz = self.quiz_generator.generate_quiz()
        self.current_question_index = 0
        self.score = 0
        self.n_o_q = 0
        self.incorrect_count = 0

        self.root = tk.Tk()
        self.root.title("Dental Quiz App - Resizable")
        self.root.configure(background="#F0F0F0")  # A lighter, more neutral background
        self.root.minsize(380, 550)  # Set a practical minimum size

        # --- Configure root window grid to be responsive ---
        self.root.columnconfigure(0, weight=1)  # Main content column expands
        self.root.rowconfigure(0, weight=1)  # Main content frame row expands
        self.root.rowconfigure(1, weight=0)  # Status bar row fixed size

        # --- Main Frame for all content ---
        main_frame = tk.Frame(self.root, bg=self.root.cget('bg'))
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # Configure main_frame's grid layout
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=0)  # Question label (auto-size height)
        main_frame.rowconfigure(1, weight=1)  # Options frame (expandable height)
        main_frame.rowconfigure(2, weight=0)  # Feedback label (auto-size height)
        main_frame.rowconfigure(3, weight=0)  # Next button (fixed height)

        # --- Question Label ---
        self.question_label = tk.Label(main_frame, text="", wraplength=350, justify="left",
                                       font=("Arial", 16, "bold"), bg=main_frame.cget('bg'), fg="#333333")
        self.question_label.grid(row=0, column=0, sticky="ew", pady=(10, 20))

        # --- Options Frame ---
        self.options_frame = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        self.options_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.options_frame.columnconfigure(0, weight=1)  # Buttons expand horizontally

        self.options_buttons = []
        for i in range(6):  # Assuming max 4 options
            self.options_frame.rowconfigure(i, weight=1)  # Distribute vertical space for buttons
            button = tk.Button(self.options_frame, text="",
                               command=lambda i=i: self.check_answer(i),
                               font=("Arial", 14), bg="#00796B", fg="white",
                               activebackground="#004D40", activeforeground="white",
                               relief=tk.FLAT, borderwidth=0, highlightthickness=0,
                               wraplength=300)  # Add wraplength to buttons too
            button.grid(row=i, column=0, sticky="ew", pady=6, ipady=10)  # ipady for internal padding
            self.options_buttons.append(button)

        # --- Feedback Label ---
        self.feedback_label = tk.Label(main_frame, text="", font=("Arial", 14),
                                       bg=main_frame.cget('bg'), wraplength=350)
        self.feedback_label.grid(row=2, column=0, sticky="ew", pady=10)

        # --- Next Button ---
        self.next_button = tk.Button(main_frame, text="Next Question",
                                     command=self.next_question, font=("Arial", 14, "bold"),
                                     bg="#FFC107", fg="#333333", relief=tk.FLAT,
                                     activebackground="#FFA000", borderwidth=0, highlightthickness=0)
        self.next_button.grid(row=3, column=0, sticky="ew", pady=(15, 5), ipady=10)

        # --- Status Bar (Optional, but good for UX) ---
        self.status_bar_frame = tk.Frame(self.root, bg="#DDDDDD", relief=tk.SUNKEN, bd=1)
        self.status_bar_frame.grid(row=1, column=0, sticky="ew")  # Placed in the second row of the root
        self.status_label = tk.Label(self.status_bar_frame, text=f"Question: 0/{len(self.quiz)} Score: 0",
                                     font=("Arial", 10), bg="#DDDDDD")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)

        # Bind resize event to adjust wraplengths
        self.root.bind("<Configure>", self.on_window_resize)

        if not self.quiz:
            messagebox.showerror("Quiz Error", "No questions loaded or available. Exiting.")
            self.root.destroy()
            return

        self.show_question()
        print(f"Initial: Total Attempted: {self.n_o_q}, Correct: {self.score}")
        self.root.mainloop()

    def on_window_resize(self, event=None):
        # Update wraplength for question_label, feedback_label, and option buttons
        # Calculate available width within the main_frame, considering padding
        try:
            # For question and feedback labels, use main_frame width
            available_width = self.main_frame.winfo_width() - 30  # Subtract main_frame's own padding
            if available_width < 100: available_width = 100

            self.question_label.config(wraplength=max(100, available_width))
            self.feedback_label.config(wraplength=max(100, available_width))

            # For option buttons, use options_frame width
            button_available_width = self.options_frame.winfo_width() - 20  # Subtract options_frame's internal padding
            if button_available_width < 80: button_available_width = 80

            for btn in self.options_buttons:
                btn.config(wraplength=max(80, button_available_width))
        except tk.TclError:
            # This can happen if widgets are not fully drawn yet (e.g., during init)
            pass

    def show_question(self):
        if not self.quiz or self.current_question_index >= len(self.quiz):
            self.show_final_score()
            return

        current_question_data = self.quiz[self.current_question_index]
        self.question_label.config(text=current_question_data["question"])

        options = current_question_data["options"]
        for i in range(len(self.options_buttons)):
            if i < len(options):
                self.options_buttons[i].config(text=options[i], state=tk.NORMAL, bg="#00796B")
                self.options_buttons[i].grid()  # Ensure button is visible
            else:
                self.options_buttons[i].grid_remove()  # Hide unused buttons

        self.feedback_label.config(text="")
        self.next_button.config(state=tk.DISABLED)
        self.update_status_bar()

        # Crucial: Allow Tkinter to process pending geometry changes before resizing
        self.root.update_idletasks()
        # Store main_frame reference if not already done (better to do in __init__)
        if not hasattr(self, 'main_frame'):
            # This is a fallback, ideally main_frame is self.main_frame
            self.main_frame = self.question_label.master
        self.on_window_resize()

    def check_answer(self, option_index):
        current_question_data = self.quiz[self.current_question_index]
        selected_answer = current_question_data["options"][option_index]
        correct_answer = current_question_data["correct_answer"]
        self.n_o_q += 1

        for btn in self.options_buttons:  # Disable all buttons after a choice
            btn.config(state=tk.DISABLED)

        if selected_answer == correct_answer:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="green")
            self.options_buttons[option_index].config(bg="#4CAF50")  # Green for correct
        else:
            self.incorrect_count += 1
            self.feedback_label.config(text=f"Incorrect. Correct answer was: {correct_answer}", fg="red",
                                       wraplength=self.feedback_label.winfo_width() - 10)
            self.options_buttons[option_index].config(bg="#F44336")  # Red for selected incorrect
            # Highlight the correct answer if a wrong one was chosen
            for i, opt_text in enumerate(current_question_data["options"]):
                if opt_text == correct_answer:
                    self.options_buttons[i].config(bg="#AED581")  # Lighter green for unselected correct
                    break

        print(f"Attempt {self.n_o_q}: True={self.score}, Incorrect={self.incorrect_count}")
        self.next_button.config(state=tk.NORMAL)
        self.update_status_bar()

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.quiz):
            self.show_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        messagebox.showinfo("Quiz Finished",
                            f"Quiz Over!\n\nYour final score: {self.score} out of {len(self.quiz)}\n"
                            f"Correct Answers: {self.score}\n"
                            f"Incorrect Answers: {self.incorrect_count}")
        self.root.destroy()

    def update_status_bar(self):
        q_num_display = self.current_question_index + 1
        total_q = len(self.quiz)
        if q_num_display > total_q and total_q > 0:
            q_num_display = total_q  # Cap display at total questions if quiz ended
        elif total_q == 0:
            q_num_display = 0  # Handle case of no questions

        self.status_label.config(text=f"Question: {q_num_display}/{total_q}  Score: {self.score}")

# Example Usage
if __name__ == "__main__":
    generator = QuizGenerator()
    app = QuizApp(generator)
