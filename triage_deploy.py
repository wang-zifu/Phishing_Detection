from detection.triage import Triage

def triage_deployement(consumer_t, producer_t_inside_boundary, producer_t_outside_boundary):
    triage = Triage()
    # Consume Predictions
    core_decision_consumer = triage.get_consumer_json(consumer_t, 'test')

    triage.set_producer()

    for data in core_decision_consumer:

        prob_ben = float(data.value['proabilities_benign'])
        prob_phish = float(data.value['probabilities_malicious'])
        
        prediction = data.value['prediction']
        domain = data.value['domain']

        decision = triage.decision_maker(prob_ben, prob_phish)
        print(decision)
        if not decision:
            # Produce to layer_one_output
            triage.producer_send(producer_t_inside_boundary, {
                'prediction': prediction,
                'proabilities_benign': prob_ben,
                'probabilities_malicious': prob_phish,
                'domain': domain,
                'triage': 0})
        # Produce to layer_two_output
        else:
            triage.producer_send(producer_t_outside_boundary, {
                'prediction': prediction,
                'proabilities_benign': prob_ben,
                'probabilities_malicious': prob_phish,
                'domain': domain,
                'triage': 1})
