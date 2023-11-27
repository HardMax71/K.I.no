from app.training import run_training, run_eval
from app.training import get_after_covid
from app.training import get_model, get_encoder
from app.training import predict_attendance
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV


after_covid = get_after_covid()
linreg_param_grid = {'copy_X': [True, False], 'fit_intercept': [True, False], 'positive': [True, False]}
grad_param = {
    "loss":['squared_error', 'absolute_error', 'huber'],
    "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
    "min_samples_split": [0.1, 0.3, 0.5],
    "min_samples_leaf": [0.1, 0.3, 0.5],
    "max_depth":[3,5,8],
    "max_features":["log2","sqrt"],
    "subsample":[0.5, 0.8, 0.9, 1.0],
    "criterion": ['friedman_mse', 'squared_error'],
    "n_estimators":[10]
    }

model = GridSearchCV(estimator=GradientBoostingRegressor(), param_grid=grad_param, 
                     cv=5, scoring='neg_mean_absolute_error', verbose=2)


def train():
    run_training(after_covid, model)

def eval():
    sel_model = get_model(model)
    enc = get_encoder()
    run_eval(after_covid, sel_model, enc)
    return 

def prediction():
    search = "All the Beauty and the Bloodshed"
    date = "21.11.2023"
    sel_model = get_model(model)
    enc = get_encoder()
    
    print(predict_attendance(search, date, sel_model, enc))

if __name__ == "__main__":
    train()
    eval()
    prediction()