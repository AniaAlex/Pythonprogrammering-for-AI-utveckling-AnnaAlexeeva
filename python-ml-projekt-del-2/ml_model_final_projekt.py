import tensorflow as tf
from tensorflow.keras.models import load_model
from typing import List, Tuple
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
import logging
import json
import os
from datetime import datetime


"""Konfigurera logging.
"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)


class ModelManager:
    """
    Klass för att hantera sparning och laddning av modellen.
    (c)läromedel
    """
    def __init__(self, base_path: str="models"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def save_model(self, model: any, model_name:str):
        """
        Sparar en modell i lämpligt format baserat på typ.

        Args:
            model: Modellen som ska sparas
            model_name: Namnet på modellen
            model_type: Typ av modell ('h5')
        (c)läromedel
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_path = os.path.join(self.base_path,model_name, f"{timestamp}")

        try:
            model.save(f"{full_path}.h5")
            # Spara metadata
            metadata = {
                'model_type': "h5",
                'timestamp': timestamp,
            }
            with open(f"{full_path}_metadata.json", 'w') as f:
                json.dump(metadata, f)

            logger.info(f"Modell sparad: {full_path}")

        except Exception as e:
            logger.error(f"Fel vid sparning av modell: {str(e)}")
            raise

    def load_model(self, model_path: str):
        """
        Laddar en modell från fil.
        """
        try:
            model=load_model(model_path)
            return model
        except Exception as e:
            logger.error(f"Fel vid laddning av modell: {str(e)}")
            raise

class DiabetesPredictionWomenModel:
    def __init__(self,  df: pd.DataFrame, parameter_list: List[str],random_state: int=42, test_size: float=0.2):
        self.scaler=StandardScaler()
        self.df=df
        self.parameter_list=parameter_list
        self.x_train=None
        self.x_test=None
        self.y_train=None
        self.y_test=None
        self.y=None
        self.x=None
        self.model = None
        self.history=None
        self.test_size=test_size
        self.random_state=random_state


    @staticmethod
    def check_params(df: pd.DataFrame, parameter_list: List[str])->None:
        """Kontrollera att alla nödvändiga
        parametrar finns på plats"""
        if not all(col in df.columns for col in parameter_list):
            logger.error(f"Saknade obligatoriska kolumner: {', '.join(parameter_list)}")
            raise ValueError(f"Saknade obligatoriska kolumner: {', '.join(parameter_list)}")
        return

    @classmethod
    def load_df(cls, file_path:str, parameter_list: List[str])->"DiabetesPredictionWomenModel":
        """Laddar datan från csv fil"""
        try:
            df = pd.read_csv(file_path)
        #Den angivna filen finns inte
        except FileNotFoundError as e:
            logger.error(str(e))
            raise
        except pd.errors.EmptyDataError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f'Fel vid ladning av filen:{str(e)}')
            raise

        cls.check_params(df,parameter_list)
        instance=cls(df,parameter_list)
        instance.x = df.drop(["Outcome"], axis=1)
        instance.y=df["Outcome"]

        return instance

    def scale_split(self)->None:
        """
           Skalera funktioner
           använder StandardScaler, orsaken:
           -Variablerna är kontinuerliga;
           -Extrema avvikelser togs bort, men
           det finns små avvikelser som kan påverka MinMax-scaling;

        """
        x_scaled = self.scaler.fit_transform(self.x)

        # Split data
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x_scaled, self.y, test_size=self.test_size, random_state=self.random_state)
        return

    def build_model(self,input_shape: int=8):
        """
        - Antal noder: baserat på antalet faktorer och flera tester;
        - Antal lager: Input och Hidden: valda utifrån datastorlek och flera tester;
        - Antal utgångslager: bestäms av typen av klassificeringsproblem: binär klassificering;
        - Det finns två olika outputs: diabetes=True, diabetes=False;
        - Sigmoid-aktivering och binary crossentropy loss fungerar bra tillsammans för binär klassificering:
        - Sigmoid-aktivering: ger sannolikheter för True-värde;
        - Binary crossentropy loss: mäter skillnaden mellan den förutsagda
          sannolikheten och den faktiska binära etiketten (0 eller 1).
        """
        model = Sequential([
            Input(shape=(8,)),
            Dense(8, activation='relu'),
            Dense(6, activation='relu'),
            Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy", "mae"])
        self.model=model
        return self.model

    def train_model(self, epochs: int = 100, batch_size: int = 32, validation_split: float = 0.2):
        """
        Träna modellen och returnera träningshistoriken
        """
        self.history = self.model.fit(self.x_train, self.y_train, epochs=epochs, batch_size=batch_size,
                            validation_split=validation_split, verbose=1)
        return self.history

    def evaluate_model(self)-> Tuple[float, float, float]:
        """
        Utvärdera modellen på testdata och returnera metrikarna.
        """
        loss, accuracy, mae = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print(f"Test accuracy: {accuracy}")
        self.model.summary()
        return loss, accuracy, mae

    def plot_history(self)->None:

        pd.DataFrame(self.history.history).plot()
        plt.ylabel("loss")
        plt.xlabel("epochs")
        plt.title("Model Training Loss")
        plt.show()
        return

    def use_model_test_data(self)->None:
        """
        Använder modellen på testdata och bygger en plot
        """
        model_predict = self.model.predict(self.x_test[0:])

        x_axis = tf.range(0, len(self.x_test))

        y_axis = self.y_test.to_numpy()
        y_axis = tf.cast(y_axis, tf.float32)

        model_predict= tf.cast(model_predict, tf.float32)

        plt.figure(figsize=(10, 7))
        plt.scatter(x_axis, y_axis, c='g', label="Testdata")

        plt.scatter(x_axis, model_predict, c='r', label="Förutsägelser")

        plt.legend()
        plt.show()
        return




def latest_file(base_path: str, extension: str):
    """
    Laddar den senast skapade modellen från den angivna mappen.
    """
    if not extension:
        logger.error("Saknade extension")
        raise ValueError("Saknade extension")

    #  Hämta alla h5 filer i den angivna mappen
    if not base_path:
        logger.error("Saknade base path")
        raise ValueError("base_path är tom")
    try:
        model_files = [f for f in os.listdir(base_path) if f.endswith(extension)]
    except FileNotFoundError as e:
        logger.error(str(e))
        raise
    if not model_files:
        logger.error(f"Ingen fil med sådan filändelse {extension} hittades")
        raise FileNotFoundError(f"Ingen fil med sådan filändelse  {extension} hittades")


    timestamps=[os.path.splitext(timestamp)[0] for timestamp in model_files ]


    # Konvertera alla tidstämpel till ett datatime-objekt
    dt_objects = [datetime.strptime(ts, "%Y%m%d_%H%M%S") for ts in timestamps]

    # Hitta den senaste tidstämpel
    latest_dt = max(dt_objects)

    # Hitta den motsvarande ursprungliga tidstämpeln
    latest_timestamp = latest_dt.strftime("%Y%m%d_%H%M%S")
    return latest_timestamp


def main():
    file_path="data_diabetes.csv"
    parameter_list = ["Glucose_imputed", "SkinThickness_imputed", "Insulin_imputed", "Age",
                      "Outcome", "BMI","BloodPressure", "Pregnancies", "DiabetesPedigreeFunction"]
    dpw=DiabetesPredictionWomenModel.load_df(file_path, parameter_list)
    print(dpw.df.describe().T.to_string())
    dpw.scale_split()
    dpw.build_model()
    dpw.train_model()
    dpw.evaluate_model()
    dpw.plot_history()
    dpw.use_model_test_data()


    model_manager = ModelManager()

    # Spara modeller
    logger.info("Sparar modeller")
    model_manager.save_model(dpw.model, "diabetes_predictor")


    file_to_load=""
    if not file_to_load:
        file_to_load=latest_file("models/diabetes_predictor/",".h5")
    logger.info(f"Modell-laddning {file_to_load}")
    loaded_model = model_manager.load_model(
        f"models/diabetes_predictor/{file_to_load}.h5",
    )






if __name__=="__main__":
    main()











