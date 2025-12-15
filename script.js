const channelID = 'UCboXCsBUZvek5T5cCltHS5w';
const backupVideoId = 'ti2DIoIAjHQ';
const backupTitle = 'ADescentrar las relaciones (Video Destacado)';

const rssUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelID}`;
const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`;

document.addEventListener('DOMContentLoaded', cargarVideoReciente);

async function cargarVideoReciente() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        let videoElegido = null;

        // Si hay al menos dos videos, muestra el segundo más reciente.
        if (data.items && data.items.length > 1) {
            videoElegido = data.items[1]; // El segundo video de la lista
        } 
        // Si solo hay uno, muestra ese.
        else if (data.items && data.items.length > 0) {
            console.log("Solo se encontró un video, mostrando el más reciente.");
            videoElegido = data.items[0]; 
        }

        if (videoElegido) {
            const videoId = videoElegido.link.split('v=')[1];
            mostrarVideo(videoId, videoElegido.title, videoElegido.pubDate);
        } else {
            throw new Error("No se encontraron videos en el feed.");
        }
    } catch (error) {
        console.error("Error cargando el feed de videos:", error);
        mostrarVideo(backupVideoId, backupTitle, "");
    }
}

function mostrarVideo(id, titulo, fecha) {
    const videoFrame = document.getElementById('main-video');
    const titleElement = document.getElementById('video-title');
    const dateElement = document.getElementById('video-date');

    if (videoFrame) {
        videoFrame.src = `https://www.youtube.com/embed/${id}`;
    }
    if (titleElement) {
        titleElement.innerText = titulo;
    }
    if (dateElement) {
        if (fecha) {
            const dateObj = new Date(fecha);
            dateElement.innerText = dateObj.toLocaleDateString('es-ES', { 
                year: 'numeric', month: 'long', day: 'numeric' 
            });
        } else {
            dateElement.innerText = '';
        }
    }
}
