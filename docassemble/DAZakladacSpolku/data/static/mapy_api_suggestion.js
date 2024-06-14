const API_KEY = 'MmUycQlxsgemcJH1XgrYu9bsbxXJr7SA6GAqJcAyrwY';
const inputElems = document.querySelectorAll(".addressAutocomplete");

inputElems.forEach(inputElem => {
    const autoCompleteJS = new autoComplete({
        selector: () => inputElem,
        placeHolder: "Vyplňte adresu…",
        searchEngine: (query, record) => `<mark>${record}</mark>`,
        data: {
            keys: ["value"],
            src: async(query) => {
                try {
                    const fetchData = await fetch(`https://api.mapy.cz/v1/suggest?lang=cs&limit=5&type=regional.address&apikey=${API_KEY}&query=${query}&locality=cz`);
                    const jsonData = await fetchData.json();

                    return jsonData.items.map(item => ({
                        value: item.name,
                        data: item,
                    }));
                } catch (exc) {
                    console.log(exc);

                    return [];
                }
            },
            cache: false,
        },
        resultItem: {
            element: (item, data) => {
                const itemData = data.value.data;
                const desc = document.createElement("div");

                desc.style = "overflow: hidden; white-space: nowrap; text-overflow: ellipsis;";
                desc.innerHTML = `${itemData.location}`;
                item.append(
                    desc,
                );
            },
            highlight: true
        },
        resultsList: {
            element: (list, data) => {
                list.style.maxHeight = "max-content";
                list.style.overflow = "hidden";

                if (!data.results.length) {
                    const message = document.createElement("div");

                    message.setAttribute("class", "no_result");
                    message.style = "padding: 5px";
                    message.innerHTML = `<span>Found No Results for "${data.query}"</span>`;
                    list.prepend(message);
                } else {
                    const logoHolder = document.createElement("div");
                    const text = document.createElement("span");
                    const img = new Image();

                    logoHolder.style = "padding: 5px; display: flex; align-items: center; justify-content: end; gap: 5px; font-size: 12px;";
                    text.textContent = "Powered by";
                    img.src = "https://api.mapy.cz/img/api/logo-small.svg";
                    img.style = "width: 60px";
                    logoHolder.append(text, img);
                    list.append(logoHolder);
                }
            },
            noResults: true,
        },
    });

    inputElem.addEventListener("selection", event => {
        // "event.detail" carries the autoComplete.js "feedback" object
        const origData = event.detail.selection.value.data;
        // data to debug
        console.log(origData);
        
        let street = "";
        let address = "";
        let municipality = "";

        origData.regionalStructure.forEach(item => {
            if (item.type === "regional.street") {
                street = item.name;
            }
            if (item.type === "regional.address") {
                address = item.name;
            }
            if (item.type === "regional.municipality") {
                municipality = item.name;
            }
        });

        inputElem.value = `${origData.name}, ${origData.zip} ${municipality}`;
    });
});