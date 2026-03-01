from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)
    
    print("MSE:", mean_squared_error(y_test, preds))
    print("MAE:", mean_absolute_error(y_test, preds))
    print("R2:", r2_score(y_test, preds))
    
    return preds


def plot_actual_vs_predicted(y_test, preds):
    plt.figure(figsize=(10,5))
    plt.plot(y_test.values, label='Actual')
    plt.plot(preds, label='Predicted')
    plt.legend()
    plt.title("Actual vs Predicted Sales Revenue")
    plt.savefig("../images/Actual VS Predicted Sales Revenue.png", dpi=300,bbox_inches="tight")
    plt.show()
    plt.close()


def plot_residuals(y_test, preds):
    residuals = y_test - preds
    sns.histplot(residuals, bins=30)
    plt.title("Residual Distribution")
    plt.show()   