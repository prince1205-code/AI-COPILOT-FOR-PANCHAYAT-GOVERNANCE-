# AI-COPILOT-FOR-PANCHAYAT-GOVERNANCE-
THIS AI WILL HELP LOCAL PEOPLE TO CONNECT WITH THE GOVERMENT. AND TAKE PART IN EVERY DECISION WHICH ARE TAKEN BY THE GOVERNMENT. THEY CAN ACCESS THROUGH ANYY 22 OFFICIAL LANGUAGE. 
THIS CODE WILL HELP TO TYPE APPLICATION. 

from fpdf import FPDF
from datetime import datetime

# Function to generate the PDF letter
def generate_letter_pdf(name, address, subject, body_text, output_file="output_letter.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.cell(200, 10, txt="Panchayat Office", ln=1, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Date: {datetime.today().strftime('%d-%m-%Y')}", ln=2, align="R")

    pdf.ln(10)  # space

    # Address and Subject
    pdf.multi_cell(200, 10, txt=f"To,\nThe Sarpanch,\nVillage Panchayat,\n{address}\n\nSubject: {subject}\n")

    pdf.ln(5)

    # Body
    pdf.multi_cell(200, 10, txt=body_text)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Thank you.", ln=1)
    pdf.cell(200, 10, txt="Yours sincerely,", ln=1)
    pdf.cell(200, 10, txt=name, ln=1)

    pdf.output(output_file)
    print(f"PDF generated successfully: {output_file}")

# Main script: get all inputs via keyboard input and generate PDF
if __name__ == "__main__":
    print("=== Panchayat Letter Generator ===")
    print("Please provide the following information:")
    print()
    
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    subject = input("Enter the subject of the letter: ")
    
    body = (
        f"I am a resident of your Panchayat and I wish to apply for the {subject}.\n"
        "I fulfill all eligibility criteria and request you to kindly consider my application.\n"
        "Enclosures: Aadhar card, age proof, income certificate."
    )

    generate_letter_pdf(name, address, subject, body)
