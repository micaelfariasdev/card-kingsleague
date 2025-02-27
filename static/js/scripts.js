let chargeteam = document.querySelector('select#id_time')
let divimgteam = document.querySelector('.team-logo')

chargeteam.addEventListener('change', function(e){
    let team = e.target.value

    divimgteam.style.backgroundImage = `url('/static/img/teams/${team}.webp')`;
})

let values = document.querySelectorAll('span[type="value_stats"]');
let pos = document.querySelector('select#id_posicao');
let overall = document.querySelector('#over_all_value');
let sliders = document.querySelectorAll('input[type="range"]');

// Função para calcular o Overall com base nos valores dos sliders e pesos
function calcularOverall() {
    let posi = pos.value; // Pega o valor atual da posição
    let pesos = {
        "GK": {"defesa": 0.5, "passe": 0.1, "habilidade": 0.1, "chute": 0.05, "duelo": 0.1, "fisico": 0.15},
            "MEI": {"defesa": 0.1, "passe": 0.3, "habilidade": 0.3, "chute": 0.2, "duelo": 0.05, "fisico": 0.05},
            "ATA": {"defesa": 0.05, "passe": 0.05, "habilidade": 0.1, "chute": 0.5, "duelo": 0.2, "fisico": 0.1},
            "DEF": {"defesa": 0.45, "passe": 0.05, "habilidade": 0.05, "chute": 0.05, "duelo": 0.2, "fisico": 0.2},
    };
    
    let overr = 0;
    sliders.forEach(slider => {
        let att = slider.value * pesos[posi][slider.name]; // Multiplica o valor do slider pelo peso da posição
        overr += Number(att);
    });

    // Atualiza o valor de Overall
    overall.innerText = Math.ceil(overr);
}

// Evento para mudança na posição
pos.addEventListener('change', () => {
    calcularOverall(); // Recalcula o Overall ao mudar a posição
});

// Evento para mudança nos sliders
sliders.forEach(slider => {
    let id = slider.id;  // Pega o id do slider
    let valorDisplay = document.getElementById("v_" + id);  // Seleciona o valor associado ao slider
    
    // Atualiza o valor ao carregar a página
    valorDisplay.innerText = slider.value;
    
    // Atualiza o valor quando o slider é movido
    slider.addEventListener("input", function() {
        valorDisplay.innerText = slider.value; // Exibe o valor atual do slider
        
        // Recalcula o Overall sempre que o slider for movido
        calcularOverall();
    });
});

// Recalcula o Overall ao carregar a página
calcularOverall();






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