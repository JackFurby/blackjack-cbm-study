from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def get_consent_pdf(strings, form_path):
	"""
	Return PdfWriter object for a completed consent form when provided with a list of elements to add
	"""

	packet = io.BytesIO()
	can = canvas.Canvas(packet, pagesize=letter)
	can.drawString(485, 496, strings[0])
	can.drawString(485, 427, strings[1])
	can.drawString(485, 359, strings[2])
	can.drawString(485, 282, strings[3])
	can.drawString(485, 227, strings[4])
	can.drawString(485, 162, strings[5])
	can.drawString(485, 95, strings[6])
	can.showPage()  # start a new page
	can.drawString(485, 716, strings[7])
	can.drawString(60, 675, strings[8])
	can.drawString(240, 675, strings[9])
	can.drawString(385, 675, strings[8])
	can.drawString(60, 580, "Jack Furby")
	can.drawString(240, 580, strings[9])
	can.drawString(385, 580, "Jack Furby")
	can.drawString(60, 514, "Principal Investigator")
	can.save()

	# move to the beginning of the StringIO buffer
	packet.seek(0)

	# create a new PDF with Reportlab and return it
	new_pdf = PdfReader(packet)

	# read your existing PDF
	existing_pdf = PdfReader(open(form_path, "rb"))
	output = PdfWriter()
	# add the "watermark" (which is the new pdf) on the existing page
	for x in range(len(existing_pdf.pages)):
		page = existing_pdf.pages[x]
		page.merge_page(new_pdf.pages[x])
		output.add_page(page)

	# convert pdf to BytesIO
	pdf = io.BytesIO()
	output.write(pdf)
	pdf.seek(0)

	return pdf


if __name__ == '__main__':
	output = get_consent_pdf(["1", "2", "3", "4", "5", "6", "7", "8", "Name", "Date"], "static/Consent-Form.pdf")

	#new_pdf = PdfReader(output)

	#output_stream = open("destination2.pdf", "wb")
	#new_pdf.write(output_stream)
	#output_stream.close()
