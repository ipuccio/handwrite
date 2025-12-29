"""Flask web application for Handwrite font generation."""
import logging
import os
import tempfile
import shutil
import uuid

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

from handwrite.cli import converters

# Load environment variables from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Configuration
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["MAX_CONTENT_LENGTH"] = int(
    os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
)  # Default: 16MB max file size

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    """Render the main upload page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_font():
    """Handle file upload and generate font."""
    if "file" not in request.files:
        flash("No file uploaded")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Invalid file type. Please upload a PNG or JPG image.")
        return redirect(url_for("index"))

    # Get optional font name from form
    font_name = request.form.get("font_name", "MyHandwriting")
    # Sanitize font name - only allow alphanumeric characters and spaces
    font_name = "".join(c for c in font_name if c.isalnum() or c == " ")
    if not font_name:
        font_name = "MyHandwriting"

    # Create unique temporary directories for this request
    request_id = str(uuid.uuid4())
    temp_upload_dir = tempfile.mkdtemp(prefix=f"handwrite_upload_{request_id}_")
    temp_output_dir = tempfile.mkdtemp(prefix=f"handwrite_output_{request_id}_")

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(temp_upload_dir, filename)
        file.save(upload_path)

        # Generate metadata
        metadata = {"filename": font_name, "family": font_name, "style": "Regular"}

        # Run the converter
        converters(upload_path, temp_output_dir, metadata=metadata)

        # Find the generated TTF file
        ttf_files = [f for f in os.listdir(temp_output_dir) if f.endswith(".ttf")]
        if not ttf_files:
            flash("Font generation failed. Please check your handwriting sample.")
            return redirect(url_for("index"))

        ttf_path = os.path.join(temp_output_dir, ttf_files[0])

        # Return the font file for download
        return send_file(
            ttf_path,
            as_attachment=True,
            download_name=f"{font_name}.ttf",
            mimetype="font/ttf",
        )

    except Exception as e:
        logger.exception("Font generation failed")
        flash("An error occurred during font generation. Please try again with a valid handwriting sample.")
        return redirect(url_for("index"))

    finally:
        # Clean up temporary directories
        shutil.rmtree(temp_upload_dir, ignore_errors=True)
        shutil.rmtree(temp_output_dir, ignore_errors=True)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
