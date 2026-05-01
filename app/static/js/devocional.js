const audio = document.getElementById("audio");
const playBtn = document.getElementById("play");
const progress = document.querySelector(".progress");
const progressContainer = document.querySelector(".progress-container");

let isPlaying = false;

playBtn.addEventListener("click", () => {
    if (isPlaying) {
        audio.pause();
        playBtn.innerText = "▶";
    } else {
        audio.volume = 0.3;
        audio.play();
        playBtn.innerText = "⏸";
    }
    isPlaying = !isPlaying;
});

audio.addEventListener("timeupdate", () => {
    const percent = (audio.currentTime / audio.duration) * 100;
    progress.style.width = percent + "%";
});

progressContainer.addEventListener("click", (e) => {
    const width = progressContainer.clientWidth;
    const clickX = e.offsetX;
    audio.currentTime = (clickX / width) * audio.duration;
});

$(document).ready(function () {
    audio.volume = 0;
    audio.play();
    isPlaying = !isPlaying;
    playBtn.innerText = "⏸";

    let vol = 0;
    let interval = setInterval(() => {
        if (vol < 0.3) {
            vol += 0.01;
            audio.volume = vol;
        } else {
            clearInterval(interval);
        }
    }, 100);
    fetch('/api/streak')
        .then(res => res.json())
        .then(data => {
            const streakNumberElement = document.querySelector('.streak-number');
            if (data.streak == 0) {
                streakNumberElement.innerHTML = 'Começe hoje a caminhar com o Senhor 🙏';
            } else {
                streakNumberElement.innerHTML = 'Há ' + data.streak + ' dia(s) com Deus! Continue Firme! 🙌'
            }
        })
})

function change_music(name, song, artist, tipo) {
    pasta = ''
    switch (tipo) {
        case 'lo-fi':
            pasta = 'lo-fi'
            break;
        case 'ambiente':
            pasta = 'ambiente'
            break;
        case 'worship':
            pasta = 'worship'
            break;
    }
    audio.src = `../../static/audio/devocional/${pasta}/${name}`;
    audio.load()

    $('.songs-name').text(song);
    $('.artist-name').text(artist);

    audio.play().then(() => {
        isPlaying = true;
        playBtn.innerText = "⏸";
        const toastTrigger = document.getElementById('liveToastBtn').click();
        document.querySelector('.text-toast').textContent = 'Aperte ESC para sair do modo playlist!';
    });
}

$(document).ready(function () {
    fetch('/api/devocional')
        .then(res => res.json())
        .then(data => {
            if (data.status == 1) {

                const source = data.source[0]
                const v = source.text

                $('#livro').text(`${source.nome_livro} ${source.capitulo}`)

                const p = document.getElementById('text');
                v.forEach(v => {
                    let d = v.split('.')
                    p.innerHTML += `
                        <p id='versiculo'><small>${d[0]}</small>${d[1]}</p>
                        `
                });

                $('#anotacao_ref').text(`${source.nome_livro} ${source.capitulo} - ${source.versiculos_inicio}:${source.versiculos_fim}`)
            }
        })
})

const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    toastTrigger.addEventListener('click', () => {
        toastBootstrap.show()
    })
}

function fecharModal(cl) {
    document.getElementById(cl).classList.add('hidden');
}

document.querySelectorAll(".cores button").forEach(btn => {
    btn.addEventListener("click", () => {
        document.getElementById("corEscolhida").value = btn.dataset.cor;
    });
});

document.querySelectorAll(".cores button").forEach(btn => {
    btn.addEventListener("click", () => {
        const cor = btn.dataset.cor;

        const card = document.querySelector(".card_notes");
        const modalContent = document.querySelector('.modal-content')
        modalContent.animate([
            { transform: "scale(1)" },
            { transform: "scale(1.05)" },
            { transform: "scale(1)" }
        ], {
            duration: 600,
            easing: "ease"
        });

        if ((cor === '#343A40') || (cor === '#3C096C') || (cor === '#1B4332') || (cor === '#2C2C54')) {
            card.style.color = 'white';
        }else {
            card.style.color = '#2c2c2c';
        }
        card.style.backgroundColor = cor;
        modalContent.style.backgroundColor = cor + '79';
    });
}); 

$(document).ready(function () {
    $('#anotacaoTitulo').on('input', function() {
        const titulo = $("#anotacaoTitulo").val();

        if (titulo != "") {
            $('#anotacaoTitle_preview').text(titulo)
        } else {
            $('#anotacaoTitle_preview').text("Insira seu Título")
        }
    })
    $('#anotacaoText').on('input', function() {
        const text = $('#anotacaoText').val();

        if (text != "") {
            $('#anotacaoText_preview').text(text)
        } else {
            $('#anotacaoText_preview').text("Coloque sua anotação aqui")
        }
    })
})