from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            sample_weight = float(request.form.get("sample_weight", 0))
            cut_fish_weight = float(request.form.get("cut_fish_weight", 0))
            total_filling_weight_425g = float(request.form.get("total_filling_weight_425g", 0))
            total_filling_weight_155g = float(request.form.get("total_filling_weight_155g", 0))
            total_filling_weight_200g = float(request.form.get("total_filling_weight_200g", 0))
            count_425g = int(request.form.get("count_425g", 0))
            count_155g = int(request.form.get("count_155g", 0))
            count_200g = int(request.form.get("count_200g", 0))

            total_filling_weight = (
                total_filling_weight_425g
                + total_filling_weight_155g
                + total_filling_weight_200g
            )
            total_can_count = count_425g + count_155g + count_200g
            waste_weight = 0.0
            waste_percentage = 0.0
            cut_fish_rate = 0.0
            recovery_rate = 0.0
            recovery = 0.0
            avg_filling_weight = 0.0
            avg_fill_425g = 0.0
            avg_fill_155g = 0.0
            avg_fill_200g = 0.0

            if sample_weight > 0:
                waste_weight = sample_weight - cut_fish_weight
                waste_percentage = (waste_weight / sample_weight) * 100
                cut_fish_rate = cut_fish_weight / sample_weight if sample_weight else 0

            if count_425g > 0:
                avg_fill_425g = total_filling_weight_425g / count_425g
            if count_155g > 0:
                avg_fill_155g = total_filling_weight_155g / count_155g
            if count_200g > 0:
                avg_fill_200g = total_filling_weight_200g / count_200g
            if total_can_count > 0:
                avg_filling_weight = total_filling_weight / total_can_count

            can_pct_425g = (count_425g / total_can_count) * 100 if total_can_count else 0
            can_pct_155g = (count_155g / total_can_count) * 100 if total_can_count else 0
            can_pct_200g = (count_200g / total_can_count) * 100 if total_can_count else 0

            fill_pct_425g = can_pct_425g - waste_percentage
            fill_pct_155g = can_pct_155g - waste_percentage
            fill_pct_200g = can_pct_200g - waste_percentage

            recovery_rate_425g = (
                (total_filling_weight_425g * 100) / fill_pct_425g
                if fill_pct_425g > 0
                else 0
            )
            recovery_rate_155g = (
                (total_filling_weight_155g * 100) / fill_pct_155g
                if fill_pct_155g > 0
                else 0
            )
            recovery_rate_200g = (
                (total_filling_weight_200g * 100) / fill_pct_200g
                if fill_pct_200g > 0
                else 0
            )

            recovery_425g = count_425g / recovery_rate_425g if recovery_rate_425g else 0
            recovery_155g = count_155g / recovery_rate_155g if recovery_rate_155g else 0
            recovery_200g = count_200g / recovery_rate_200g if recovery_rate_200g else 0

            result = {
                "sample_weight": float(f"{sample_weight:.3f}"),
                "cut_fish_weight": float(f"{cut_fish_weight:.3f}"),
                "waste_weight": round(waste_weight, 3),
                "waste_percentage": round(waste_percentage, 3),
                "total_filling_weight": total_filling_weight,
                "total_filling_weight_425g": total_filling_weight_425g,
                "total_filling_weight_155g": total_filling_weight_155g,
                "total_filling_weight_200g": total_filling_weight_200g,
                "count_425g": count_425g,
                "count_155g": count_155g,
                "count_200g": count_200g,
                "total_can_count": total_can_count,
                "avg_filling_weight": round(avg_filling_weight, 3),
                "avg_fill_425g": round(avg_fill_425g, 3),
                "avg_fill_155g": round(avg_fill_155g, 3),
                "avg_fill_200g": round(avg_fill_200g, 3),
                "can_pct_425g": round(can_pct_425g, 3),
                "can_pct_155g": round(can_pct_155g, 3),
                "can_pct_200g": round(can_pct_200g, 3),
                "fill_pct_425g": round(fill_pct_425g, 3),
                "fill_pct_155g": round(fill_pct_155g, 3),
                "fill_pct_200g": round(fill_pct_200g, 3),
                "recovery_rate_425g": round(recovery_rate_425g, 3),
                "recovery_rate_155g": round(recovery_rate_155g, 3),
                "recovery_rate_200g": round(recovery_rate_200g, 3),
                "recovery_425g": round(recovery_425g, 3),
                "recovery_155g": round(recovery_155g, 3),
                "recovery_200g": round(recovery_200g, 3),
            }
        except ValueError:
            result = {"error": "Please enter valid numeric values."}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002)