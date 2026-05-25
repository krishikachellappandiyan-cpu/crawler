class BehaviorMapper:

    def __init__(self):

        self.behaviors = []

    # --------------------------------
    # PAGE TO PAGE FLOW
    # --------------------------------

    def add_navigation(
        self,
        source,
        target
    ):

        self.behaviors.append({

            "type": "navigation",

            "source": source,

            "target": target
        })

    # --------------------------------
    # FORM SUBMISSION FLOW
    # --------------------------------

    def add_form_flow(
        self,
        page,
        action
    ):

        self.behaviors.append({

            "type": "form_submission",

            "source": page,

            "target": action
        })

    # --------------------------------
    # JS API FLOW
    # --------------------------------

    def add_api_flow(
        self,
        script,
        endpoint
    ):

        self.behaviors.append({

            "type": "api_call",

            "source": script,

            "target": endpoint
        })

    # --------------------------------
    # EXPORT
    # --------------------------------

    def export_behaviors(self):

        return self.behaviors