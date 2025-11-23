from flask import Flask, render_template, request

app = Flask(__name__)

GST_RATE = 9  # Singapore GST 9%


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        price_str = request.form.get("price_inclusive", "").strip()

        if not price_str:
            error = "Please enter a price including GST."
        else:
            try:
                price_incl = float(price_str)
                if price_incl <= 0:
                    error = "Price must be more than 0."
                else:
                    divisor = 1 + GST_RATE / 100
                    original = price_incl / divisor
                    gst_amount = price_incl - original

                    result = {
                        "price_inclusive": price_incl,
                        "original_price": original,
                        "gst_amount": gst_amount,
                    }
            except ValueError:
                error = "Please enter a valid number."

    return render_template(
        "index.html",
        gst_rate=GST_RATE,
        result=result,
        error=error,
    )


# Simple health check endpoint for UptimeRobot / Render
@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True)