const canvas = document.querySelector(".fireworks");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Firework {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.particles = [];
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: this.x,
                y: this.y,
                angle: Math.random() * 2 * Math.PI,
                speed: Math.random() * 5 + 2,
                alpha: 1,
            });
        }
    }
    update() {
        this.particles.forEach((p) => {
            p.x += Math.cos(p.angle) * p.speed;
            p.y += Math.sin(p.angle) * p.speed;
            p.alpha -= 0.02;
        });
    }
    draw() {
        this.particles.forEach((p) => {
            ctx.fillStyle = this.color;
            ctx.globalAlpha = p.alpha;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
            ctx.fill();
        });
    }
}

let fireworks = [];
let fireworkInterval = 50; // Intervalo inicial para lançar fogos de artifício
let lastLaunchTime = Date.now(); // A última vez que o foguete foi lançado

function launchFirework() {
    const currentTime = Date.now();
    // Lança um foguete apenas se passou o intervalo de tempo
    if (currentTime - lastLaunchTime >= fireworkInterval) {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height * 0.5;
        const colors = ["red", "yellow", "blue", "green", "purple", "orange"];
        const color = colors[Math.floor(Math.random() * colors.length)];
        fireworks.push(new Firework(x, y, color));
        lastLaunchTime = currentTime; // Atualiza a última vez que o foguete foi lançado
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    fireworks.forEach((firework, index) => {
        firework.update();
        firework.draw();
        if (firework.particles.every((p) => p.alpha <= 0)) {
            fireworks.splice(index, 1);
        }
    });
    requestAnimationFrame(animate);
}

setInterval(launchFirework, fireworkInterval);
animate();

// A cada 10 segundos, ajusta o intervalo de lançamento dos fogos
setTimeout(() => {
    fireworkInterval = 1500; // Aumenta o tempo entre os lançamentos (em milissegundos)
}, 5000); // Após 10 segundos

window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const course = params.get("course");
    const score = params.get("score");

    if (course) document.getElementById("course").textContent = course;
    if (score) document.getElementById("score").textContent = score;
});
