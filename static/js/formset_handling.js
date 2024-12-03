document.addEventListener('DOMContentLoaded', function() {
    let formIndex = parseInt(totalFormCount);

    const addFormButton = document.getElementById('add-form');
    const formsetContainer = document.getElementById('formset-container');
    const emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;

    addFormButton.addEventListener('click', function() {
        const newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formIndex);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newFormHtml.trim();
        const newForm = tempDiv.firstChild;
        formsetContainer.appendChild(newForm);

        formIndex++;
        document.getElementById(`id_${formsetPrefix}-TOTAL_FORMS`).value = formIndex;
    });

    formsetContainer.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('remove-form-btn')) {
            const formDiv = event.target.closest('.formset-form');
            const deleteField = formDiv.querySelector(`input[type="checkbox"][name*="-DELETE"]`);
            if (deleteField) {
                // Existing form: mark for deletion and hide
                deleteField.checked = true;
                formDiv.style.display = 'none';
            } else {
                // New form: remove from DOM
                formDiv.remove();
                formIndex--;
                document.getElementById(`id_${formsetPrefix}-TOTAL_FORMS`).value = formIndex;
                reIndexForms();
            }
        }
    });

    function reIndexForms() {
        const forms = formsetContainer.querySelectorAll('.formset-form');
        document.getElementById(`id_${formsetPrefix}-TOTAL_FORMS`).value = forms.length;
        forms.forEach((form, index) => {
            form.id = `form-${index}`;
            const fields = form.querySelectorAll('input, select, textarea, label');
            fields.forEach((field) => {
                updateElementIndex(field, index);
            });
        });
    }

    function updateElementIndex(element, index) {
        const idRegex = new RegExp(`${formsetPrefix}-(\\d+)-`);
        const replacement = `${formsetPrefix}-${index}-`;
        if (element.id) {
            element.id = element.id.replace(idRegex, replacement);
        }
        if (element.name) {
            element.name = element.name.replace(idRegex, replacement);
        }
        if (element.getAttribute('for')) {
            element.setAttribute('for', element.getAttribute('for').replace(idRegex, replacement));
        }
    }
});