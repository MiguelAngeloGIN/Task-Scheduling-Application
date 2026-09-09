from fasthtml import common as c


class TaskSearch:
    @staticmethod
    def search_bar():
        return c.Div(
            c.Label(
                'Search: ',
                c.Input(
                    type='search',
                    id='search',
                    placeholder='Search for tasks'
                )
            )
        )

    @staticmethod
    def dropdown():
        return c.Div(
            c.Ul(id='search-results'),
            c.Div(id='selected-tasks')
        )

    @staticmethod
    def auto_search(form_id, hidden_input_id, mode = "select"):
        script = """
        document.addEventListener("DOMContentLoaded", () => {
        console.log("SEARCH SCRIPT LOADED");

        let selected_storage = new Map(); 

        document.getElementById('search').addEventListener('input', async e => {

            let query = e.target.value;
            let results = document.getElementById('search-results');

            if (query.length === 0) {
                results.innerHTML = "";
                return;
            }

            let response = await fetch(`/search-tasks?query=${encodeURIComponent(query)}`);
            let tasks = await response.json();

            results.innerHTML = "";

            tasks.forEach(task => {

                let option = document.createElement("li");
                let button = document.createElement("button");

                button.textContent = task.title;
                button.type = "button";

                button.onclick = () => {
                    if ("{mode}" === "redirect") {

                    window.location.href = `/update-task/${task.id}`;

                    } else {

                    let selected = document.getElementById('selected-tasks');

                    if (!selected_storage.has(task.id)) {

                        selected_storage.set(task.id, {
                            id: task.id,
                            title: task.title
                        });

                        let chip = document.createElement("button");

                        chip.textContent = task.title;
                        chip.className = "chip";
                        chip.type = "button";
                        chip.title = "Click to remove";

                        chip.onclick = () => {
                            selected_storage.delete(task.id);
                            selected.removeChild(chip);
                        };

                        selected.appendChild(chip);
                    }
                    
                    }
                };

                option.appendChild(button);
                results.appendChild(option);

            });

        });

         if ("{mode}" === "select") {
        document.querySelector('#{form_id}').addEventListener('submit', e => {

            let hiddenInput = document.querySelector('input[id="{hidden_input_id}"]');

            let selected_ids = Array.from(selected_storage.values())
                .map(task => task.id);

            hiddenInput.value = JSON.stringify(selected_ids);

        });
        }

    });
    """

        script = script.replace("{form_id}", form_id)
        script = script.replace("{hidden_input_id}", hidden_input_id)
        script = script.replace("{mode}", mode)

        return c.Script(script)
        


    @staticmethod
    def render(form_id, hidden_input_id, mode = "select"):
        return c.Div(
            TaskSearch.search_bar(),
            TaskSearch.dropdown(),
            TaskSearch.auto_search(form_id, hidden_input_id, mode)
        )