$('#btn-submit').on('click',function(e) {
    
    e.preventDefault();
    var form = this;
    Swal.fire({
        title: 'Êtes-vous sûr?',
        text: "Vous n'aurez pas la possibilité de les modifier par la suite!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'Annulé',
        confirmButtonText: 'Oui, j\'envoie!'
   }).then((result) => {
     if (result.value == true) {
        $('#myForm').submit();
        Swal.fire("Bon boulot!", "Les résultats ont étè envoyés!", "success")
     } else {
        Swal.fire("Envoi annulé", "Les résultats n\'ont pas étè envoyés :)", "error");
     }
   });;
});