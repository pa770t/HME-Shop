const loadFile = function (event) {
    const output = document.getElementById('preview')
    output.src = URL.createObjectURL(event.target.files[0])
    output.onload = function () {
        URL.revokeObjectURL(output.src)
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('myModal');
    var open = document.getElementById('openModalBtn');
    var close = document.getElementById('close');

    open.onclick = () => {
        modal.classList.remove('d-none')
        modal.classList.remove('overflow-auto')
        modal.classList.add('d-block')
        modal.classList.add('overflow-y-hidden')
    };

    close.onclick = function() {
        modal.classList.remove('d-block')
        modal.classList.add('d-none')
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.classList.remove('d-block')
            modal.classList.add('d-none')
        }
    };
});

// document.getElementById('sort').onchange = function () {
//     window.location.hash = this.value
//     console.log(window.location.hash)
// }

const quantity = document.getElementById('quantity')
const plus = document.getElementById('plus')
const minus = document.getElementById('minus')

plus.addEventListener('click', function () {
    let current_quantity = parseInt(quantity.value)
    let new_quantity = current_quantity + 1
    quantity.value = new_quantity
})

minus.addEventListener('click', function () {
    if (quantity.value > 1) {
        let current_quantity = parseInt(quantity.value)
        let new_quantity = current_quantity - 1
        quantity.value = new_quantity
    }
})
