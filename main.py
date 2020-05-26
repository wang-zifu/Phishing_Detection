from triage_deploy import triage_deployement
from layer_one_deploy import layer_one_deploy
import os 

def config_check():
    deployement_style = os.environ.get('MACHINE_TYPE')

    if deployement_style == 0:
        triage_deployement()

    elif deployement_style == 1:
        layer_one_deploy()

    elif deployement_style == 2:
        pass
    

def main():
    # config_check()
    layer_one_deploy()
        


if __name__ == "__main__":
    main()
    
