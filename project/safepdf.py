from fpdf import FPDF
import os

def save_graphs_to_pdf(graph_files, output_pdf):
    """
    Speichert mehrere Grafiken in einem PDF-Dokument.

    Parameters:
        graph_files (list): Liste von Pfaden zu den gespeicherten Grafiken (PNG).
        output_pdf (str): Pfad zum Ausgabepdf.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for graph_file in graph_files:
        if os.path.exists(graph_file):  # Prüfen, ob die Datei existiert
            pdf.add_page()
            pdf.image(graph_file, x=10, y=20, w=180)  # Grafiken hinzufügen
        else:
            print(f"Datei nicht gefunden: {graph_file}")

    # PDF speichern
    pdf.output(output_pdf)
    print(f"Das PDF wurde erfolgreich gespeichert: {output_pdf}")

# Ordner der Grafiken
save_directory = os.path.join(os.path.dirname(__file__), "data")

# Liste der gespeicherten Grafiken
graph_files = [
    os.path.join(save_directory, "temperature_large_graph.png"),
    os.path.join(save_directory, "co2_emissions_large_graph.png"),
    os.path.join(save_directory, "temperature_vs_emissions.png"),
    os.path.join(save_directory, "temperature_trendlines.png")
]

# Ausgabe-PDF
output_pdf = os.path.join(save_directory, "grafiken.pdf")

# PDF mit allen Grafiken erstellen
save_graphs_to_pdf(graph_files, output_pdf)
