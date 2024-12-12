function agregarAlCarrito(codigo, nombreProducto) {
    fetch(`/carrito/agregar/${codigo}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: `${nombreProducto}`,
                    text: 'Agregado al carrito :D',
                    icon: 'success',
                    showCancelButton: true,
                    confirmButtonText: 'Ir a pagar',
                    cancelButtonText: 'Seguir comprando',
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Redirige a la página del carrito si el usuario hace clic en "Ir a pagar"
                        window.location.href = '/carrito/';
                    }
                    // Si se presiona "Seguir comprando", la alerta se cierra y no se realiza ninguna acción
                });
            }
        })
        .catch(error => {
            console.error('Error al agregar al carrito:', error);
        });
}

function validarEntrada(input) {
    // Expresión regular para permitir solo letras y números
    const regex = /^[A-Za-z0-9]*$/;

    // Si el valor no coincide con la expresión regular, eliminar el último carácter
    if (!regex.test(input.value)) {
        input.value = input.value.slice(0, -1);
    }
}

