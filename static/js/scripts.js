let chargeteam = document.querySelector('select#id_time')
let divimgteam = document.querySelector('.team-logo')

chargeteam.addEventListener('change', function(e){
    let team = e.target.value

    divimgteam.style.backgroundImage = `url('/static/img/teams/${team}.webp')`;
})

// let defesa = document.querySelector('input#id_defesa')
// let passe = document.querySelector('input#id_passe')
// let habilidade = document.querySelector('input#id_habilidade')
// let chute = document.querySelector('input#id_chute')
// let duelo = document.querySelector('input#id_duelo')
// let fisico = document.querySelector('input#id_fisico')

let values = document.querySelectorAll('span[type="value_stats"]');


let overall = document.querySelector('#over_all_value')

let sliders = document.querySelectorAll('input[type="range"]');

    sliders.forEach(slider => {
        let id = slider.id;  // Pega o id do slider
        let valorDisplay = document.getElementById("v_" + id);  // Seleciona o valor associado
        
        // Atualiza o valor ao carregar a página
        valorDisplay.innerText = slider.value;
        
        // Atualiza o valor quando o slider é movido
        slider.addEventListener("input", function() {
            var sum = 0
            values.forEach(slider => {
                sum += Number(slider.textContent)    
            })
    
            var over = Math.ceil(sum / values.length)
            valorDisplay.innerText = slider.value;
            overall.innerText = over 
        });
    });




let fotopreview = document.querySelector('.foto-player')
let fotoinput = document.querySelector('input#id_foto')

fotoinput.addEventListener('change', function(event) {
    const file = event.target.files[0];  
    if (file) {
        const reader = new FileReader();  
        reader.onload = function(e) {
            fotopreview.style.backgroundImage = `url('${e.target.result}')`
            
            
            fotopreview.innerHTML = '';
        };

        reader.readAsDataURL(file);  
    }
});