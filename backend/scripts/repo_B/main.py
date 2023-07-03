import os
import yaml
import pandas as pd
import xlrd
from datetime import datetime

from src.pipeline import run_pipeline



if __name__ == "__main__":
    # lecture des paramètres du fichier de configuration
    default_config_file = "config/default.yaml"
    with open(default_config_file, "r") as f:
        default_config = yaml.load(f, Loader=yaml.FullLoader)

    user_config_file = "config/user_config.yaml"
    with open(user_config_file, "r") as f:
        user_config = yaml.load(f, Loader=yaml.FullLoader)

 
    # get result from pipeline
    df_results, diag_info = run_pipeline(input_file=os.path.join(default_config["directories"]["inputs"], user_config["inputs"]["questionnaire_file"]),
                                         identification_column=user_config["inputs"]["identification_column"],
                                         scenarii_column_names=default_config["static_data"]["scenarii_column_names"],
                                         model_path=default_config["model"]["path"],
                                         class_column_name=default_config["model"]["class_column_name"])


    # export results
    with pd.ExcelWriter(os.path.join(default_config["directories"]["results"],
                                     "%s_%s_%s.xlsx" % (user_config["results"]["file"],
                                                        user_config["results"]["labo"],
                                                        datetime.today().strftime("%Y-%m-%d-%Hh%M")))) as writer:
      df_results.to_excel(writer, index=False)
