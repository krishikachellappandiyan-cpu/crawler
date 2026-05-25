class FormExtractor:

    def extract_forms(self, soup):

        forms_data = []

        forms = soup.find_all("form")

        for form in forms:

            form_info = {
                "action": form.get("action"),
                "method": form.get("method"),
                "inputs": []
            }

            inputs = form.find_all("input")

            for input_tag in inputs:

                form_info["inputs"].append({
                    "name": input_tag.get("name"),
                    "type": input_tag.get("type")
                })

            forms_data.append(form_info)

        return forms_data