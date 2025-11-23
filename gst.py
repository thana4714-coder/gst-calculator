from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Default GST rate comes from environment variable, or 9% if not set
GST_RATE_DEFAULT = float(os.getenv("GST_RATE", "9"))


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    # This is the rate we will actually use in the calculation
    used_gst_rate = GST_RATE_DEFAULT

    if request.method == "POST":
        price_str = request.form.get("price_inclusive", "").strip()
        gst_rate_str = request.form.get("gst_rate", "").strip()

        # 1. Handle GST rate input
        if gst_rate_str:
            try:
                used_gst_rate = float(gst_rate_str)
                if used_gst_rate < 0:
                    error = "GST rate cannot be negative."
            except ValueError:
                error = "Please enter a valid GST rate."

        # 2. Handle price input
        if not price_str:
            if not error:  # only overwrite if no GST error yet
                error = "Please enter a price including GST."
        else:
            try:
                price_incl = float(price_str)
                if price_incl <= 0:
                    if not error:
                        error = "Price must be more than 0."
                else:
                    if not error:  # only calculate if no previous error
                        divisor = 1 + used_gst_rate / 100
                        original = price_incl / divisor
                        gst_amount = price_incl - original

                        result = {
                            "price_inclusive": price_incl,
                            "original_price": original,
                            "gst_amount": gst_amount,
                            "gst_rate": used_gst_rate,
                        }
            except ValueError:
                if not error:
                    error = "Please enter a valid number."

    return render_template(
        "index.html",
        gst_rate_default=GST_RATE_DEFAULT,  # the default from env
        used_gst_rate=used_gst_rate,        # the rate used this time
        result=result,
        error=error,
    )


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True)