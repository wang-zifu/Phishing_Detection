from triage_deploy import triage_deployement
from layer_deploy import layer_deploy
import os 

def config_check():
    deployement_style = os.environ.get('MACHINE_TYPE')

    if deployement_style == 0:
        triage_deployement(
            consumer_t = 'test_triage',
            producer_t_inside_boundary = 'test_output'
            producer_t_outside_boundary = 'test_layer_two'
        )

    elif deployement_style == 1:
        layer_deploy(
            layer = 1,
            consumer_t = 'test_DNS',
            producer_t = 'test_triage')

    elif deployement_style == 2:
        layer_deploy(
            layer = 2,
            consumer_t = 'test_layer_two',
            producer_t = 'test_output'
        )
    

def main():
    config_check()
        


if __name__ == "__main__":
    main()
    
