use genpdf::elements::{
    Break, FramedElement, LinearLayout, PaddedElement, PageBreak, Paragraph, StyledElement,
};
use genpdf::style::Color;
use genpdf::style::Style;
use genpdf::{Alignment, Element, Margins};
use pyo3::prelude::*;
use std::path::PathBuf;

/// Collects all test details (function name, docstring, function body) and renders them to a single
/// multipage PDF
#[pyfunction]
fn create_test_pdf(test_details: Vec<Vec<String>>, pdf_path: String) -> PyResult<()> {
    let font_path = get_font_path();
    // General PDF properties
    let font_family =
        genpdf::fonts::from_files(font_path, "Roboto", None).expect("Failed to load font family");
    let mut doc = genpdf::Document::new(font_family);
    doc.set_title("Test Protocol");
    doc.set_line_spacing(1.25);

    let mut decorator = genpdf::SimplePageDecorator::new();
    decorator.set_margins(10);
    //set_header has the feature to provide the page number for every page
    // Can later be used in a format! or something but is unused for now (declared by underscore prefix)
    decorator.set_header(|_page_number| {
        Paragraph::new("Pytest Test Protocol")
            .aligned(Alignment::Center)
            .styled(Style::new().bold().with_font_size(16))
    });
    doc.set_page_decorator(decorator);
    doc.push(Break::new(1));

    // create a new page for every test (function name + docstring + function body)
    let mut entry_counter = 0;
    let n_tests = test_details.len();
    for entry in test_details {
        //function name as title
        let func_name = format!("Documented function: '{}'", entry[0].clone());
        let func_name_par = Paragraph::new(func_name);
        let bold_style = Style::new().bold().with_font_size(14);
        let func_name_bold = StyledElement::new(func_name_par, bold_style);
        doc.push(func_name_bold);
        doc.push(Break::new(1));

        //docstring in a frame
        let docstring = entry[1].clone();
        let doc_par = paragraph_with_linebreaks(&docstring);
        let doc_par_padded = doc_par;
        doc.push(doc_par_padded);
        doc.push(Break::new(1));

        //function body in a frame
        let func_body = entry[2].clone();
        let func_body_par = paragraph_with_linebreaks(&func_body);
        let func_body_par_padded = func_body_par;
        doc.push(func_body_par_padded);

        entry_counter += 1;
        if entry_counter < n_tests {
            let pagebreak = PageBreak::new();
            doc.push(pagebreak);
        }
    }

    // Write to file
    doc.render_to_file(pdf_path)
        .expect("Failed to write PDF file");

    Ok(())
}

/// Helper function to properly interpret the linebreaks in docstrings
fn paragraph_with_linebreaks(
    text: &str,
) -> StyledElement<FramedElement<PaddedElement<LinearLayout>>> {
    let mut layout = LinearLayout::vertical();
    for line in text.split('\n') {
        layout.push(
            //fixes the color of the text, so that it's not overwritten later by the frame color
            Paragraph::new(line).styled(Style::new().with_color(Color::Rgb(40, 40, 40))),
        );
    }
    layout
        .padded(Margins::all(2.0))
        .framed()
        //setting the frame color
        .styled(Style::new().with_color(Color::Rgb(150, 150, 150)))
}

///This functions makes the fonts path available after they where put into the wheel via maturin
fn get_font_path() -> PathBuf {
    Python::with_gil(|py| {
        let importlib_resources = py
            .import("importlib.resources")
            .expect("Failed to import importlib.resources");

        let font_path = importlib_resources
            .call_method1("path", ("pytest_iso", "fonts"))
            .expect("Failed to get resource path");

        let font_path_str: String = font_path
            .getattr("__enter__")
            .unwrap()
            .call0()
            .unwrap()
            .str()
            .unwrap()
            .to_string();

        PathBuf::from(font_path_str)
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn pytest_iso(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(create_test_pdf, m)?)?;
    Ok(())
}
