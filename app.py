from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os
import shap
import numpy as np


app = Flask(__name__)


# Load model files

model = joblib.load(
    "models/fraud_detection_model.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

feature_columns = joblib.load(
    "models/feature_columns.pkl"
)



# SHAP

explainer = shap.TreeExplainer(model)



UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)




@app.route("/")
def home():

    return render_template(
        "index.html"
    )




@app.route(
    "/predict_file",
    methods=["POST"]
)
def predict_file():

    try:


        file = request.files["file"]


        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )


        file.save(filepath)



        df = pd.read_csv(filepath)



        X = df[feature_columns]



        X_scaled = scaler.transform(
            X
        )



        predictions = model.predict(
            X_scaled
        )


        probabilities = model.predict_proba(
            X_scaled
        )[:,1]



        df["Prediction"] = predictions


        df["Fraud_Probability"] = (
            probabilities * 100
        ).round(2)



        df.to_csv(
            "prediction_result.csv",
            index=False
        )



        total_count = len(df)


        fraud_count = int(
            predictions.sum()
        )


        normal_count = (
            total_count - fraud_count
        )


        fraud_percentage = round(
            (fraud_count / total_count)*100,
            2
        )



        fraud_records = (

            df[df["Prediction"]==1]

            .head(10)

            .to_dict(
                orient="records"
            )

        )



        # =========================
        # SAFE SHAP
        # =========================


        shap_explanation = []



        if fraud_count > 0:


            fraud_index = list(
                df[df["Prediction"]==1].index
            )[0]



            sample = X.iloc[
                fraud_index
            ]



            sample_scaled = scaler.transform(
                pd.DataFrame(
                    [sample]
                )
            )



            shap_values = (
                explainer
                .shap_values(
                    sample_scaled
                )
            )



            # Handle SHAP versions

            if isinstance(
                shap_values,
                list
            ):

                values = shap_values[1]

            else:

                values = shap_values



            values = np.array(values)



            values = values.reshape(-1)



            # Match length

            feature_count = len(
                feature_columns
            )


            values = values[:feature_count]



            explanation = pd.DataFrame({

                "Feature":
                feature_columns[:len(values)],


                "Impact":
                values

            })



            explanation["abs"] = (
                explanation["Impact"]
                .abs()
            )


            explanation = (
                explanation
                .sort_values(
                    "abs",
                    ascending=False
                )
                .head(5)
            )


            shap_explanation = (
                explanation[
                    [
                        "Feature",
                        "Impact"
                    ]
                ]
                .to_dict(
                    orient="records"
                )
            )





        return jsonify({

            "message":
            "Prediction completed",


            "total_transactions":
            total_count,


            "fraud_transactions":
            fraud_count,


            "normal_transactions":
            normal_count,


            "fraud_percentage":
            fraud_percentage,


            "fraud_records":
            fraud_records,


            "shap_explanation":
            shap_explanation

        })



    except Exception as e:


        print(
            "ERROR:",
            e
        )


        return jsonify({

            "error":
            str(e)

        })





if __name__ == "__main__":

    app.run(
        debug=True
    )