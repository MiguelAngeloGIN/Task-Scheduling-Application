from fasthtml import common as c


class AutoSearch:

    @staticmethod
    def search_bar(search_id, label):
        return c.Div(
            c.Label(
                label,
                c.Input(
                    type='search',
                    id=search_id,
                    placeholder='Search'
                )
            )
        )

    @staticmethod
    def dropdown(search_id):
        return c.Div(
            c.Ul(id=f'{search_id}-results'),
            c.Div(id=f'{search_id}-selected')
        )

    @staticmethod
    def auto_search(form_id, hidden_input_id, entity, search_id, mode="select"):

        script = """
           console.log("AUTO SEARCH LOADED");
        document.addEventListener("DOMContentLoaded", () => {

            let selected_storage = new Map();

            let search = document.getElementById('{search_id}');
            let results = document.getElementById('{search_id}-results');
            let selected = document.getElementById('{search_id}-selected');

            search.addEventListener('input', async e => {

                let query = e.target.value;

                if (query.length === 0) {
                    results.innerHTML = "";
                    return;
                }

                let response = await fetch(`/search-{entity}?query=${encodeURIComponent(query)}`);
                let results_data = await response.json();

                results.innerHTML = "";

                results_data.forEach(result => {

                    let option = document.createElement("li");
                    let button = document.createElement("button");

                    button.textContent = result.name;
                    button.type = "button";

                    button.onclick = () => {

                        if ("{mode}" === "redirect") {

                            window.location.href = `/update-{entity}/${result.id}`;

                        } 
                        
                        if ("{mode}" === "select_one") {
                            selected_storage.clear();
                            selected.innerHTML = "";
                        }
                        
                        

                        if (!selected_storage.has(result.id)) {

                            selected_storage.set(result.id, {
                                id: result.id,
                                name: result.name
                            });


                            let chip = document.createElement("button");

                            chip.textContent = result.name;
                            chip.className = "chip";
                            chip.type = "button";
                            chip.title = "Click to remove";


                            chip.onclick = () => {
                                selected_storage.delete(result.id);
                                selected.removeChild(chip);
                            };


                            selected.appendChild(chip);
                            }
                    };


                    option.appendChild(button);
                    results.appendChild(option);

                });

            });


            if ("{mode}" === "select") {

                document.querySelector('#{form_id}')
                .addEventListener('submit', e => {

                    let hiddenInput = document.querySelector('#{hidden_input_id}');

                    let selected_ids = Array.from(selected_storage.values())
                        .map(result => result.id);


                    hiddenInput.value = JSON.stringify(selected_ids);

                });

            }
            if ("{mode}" === "select_one") {
                document.querySelector('#{form_id}')
                .addEventListener('submit', e => {
                    let hiddenInput = document.querySelector('#{hidden_input_id}');
                    let selected_id = Array.from(selected_storage.values())
                        .map(result => result.id)[0];

                    hiddenInput.value = selected_id || "";
                });
            
            }


        });
        """

        script = script.replace("{form_id}", form_id)
        script = script.replace("{hidden_input_id}", hidden_input_id)
        script = script.replace("{mode}", mode)
        script = script.replace("{entity}", entity)
        script = script.replace("{search_id}", search_id)

        return c.Script(script)


    @staticmethod
    def render(form_id, hidden_input_id, entity, search_id, label, mode="select"):

        return c.Div(
            AutoSearch.search_bar(search_id, label),
            AutoSearch.dropdown(search_id),

            c.Input(type="hidden", id=hidden_input_id, name=hidden_input_id),
            
            AutoSearch.auto_search(
                form_id,
                hidden_input_id,
                entity,
                search_id,
                mode
            )
        )



        