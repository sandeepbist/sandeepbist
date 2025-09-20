<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sandeep Bist - GitHub Profile</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

{
margin: 0;
padding: 0;
box-sizing: border-box;
font-family: 'Poppins', sans-serif;
}

body {
background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
color: #fff;
line-height: 1.6;
padding: 20px;
overflow-x: hidden;
}

.container {
max-width: 1200px;
margin: 0 auto;
}

        /* Header Styles */

.header {
text-align: center;
padding: 40px 20px;
position: relative;
overflow: hidden;
}

.profile-pic {
width: 150px;
height: 150px;
border-radius: 50%;
border: 4px solid #00F7FF;
margin: 0 auto 20px;
overflow: hidden;
position: relative;
box-shadow: 0 0 20px rgba(0, 247, 255, 0.5);
animation: float 6s ease-in-out infinite;
}

.profile-pic img {
width: 100%;
height: 100%;
object-fit: cover;
}

.header h1 {
font-size: 3rem;
margin-bottom: 10px;
background: linear-gradient(45deg, #00F7FF, #00ff95, #00F7FF);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
animation: gradient 3s ease infinite;
background-size: 200% 200%;
}

.header h2 {
font-size: 1.5rem;
margin-bottom: 20px;
color: #ccc;
}

.typing-container {
margin: 20px 0;
min-height: 60px;
}

        /* Section Styles */

.section {
background: rgba(255, 255, 255, 0.05);
border-radius: 15px;
padding: 25px;
margin-bottom: 30px;
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.1);
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.section:hover {
transform: translateY(-5px);
box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.section h2 {
font-size: 1.8rem;
margin-bottom: 20px;
color: #00F7FF;
display: flex;
align-items: center;
}

.section h2 i {
margin-right: 10px;
}

        /* Skills Grid */

.skills-grid {
display: grid;
grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
gap: 15px;
margin-top: 20px;
}

.skill-item {
background: rgba(0, 247, 255, 0.1);
border-radius: 10px;
padding: 15px 10px;
text-align: center;
transition: all 0.3s ease;
border: 1px solid rgba(0, 247, 255, 0.2);
}

.skill-item:hover {
background: rgba(0, 247, 255, 0.2);
transform: scale(1.05);
}

.skill-item img {
height: 40px;
margin-bottom: 10px;
}

        /* Stats Grid */

.stats-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
gap: 20px;
margin-top: 20px;
}

.stat-card {
background: rgba(255, 255, 255, 0.05);
border-radius: 10px;
padding: 20px;
text-align: center;
border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-card h3 {
font-size: 1.2rem;
margin-bottom: 10px;
color: #00ff95;
}

        /* Social Links */

.social-links {
display: flex;
justify-content: center;
gap: 20px;
margin-top: 20px;
}

.social-link {
display: inline-flex;
align-items: center;
justify-content: center;
width: 50px;
height: 50px;
border-radius: 50%;
background: rgba(255, 255, 255, 0.1);
color: #fff;
font-size: 1.5rem;
transition: all 0.3s ease;
text-decoration: none;
}

.social-link:hover {
background: #00F7FF;
transform: translateY(-3px);
color: #000;
}

        /* Animations */

@keyframes float {
0% { transform: translateY(0px); }
50% { transform: translateY(-10px); }
100% { transform: translateY(0px); }
}

@keyframes gradient {
0% { background-position: 0% 50%; }
50% { background-position: 100% 50%; }
100% { background-position: 0% 50%; }
}

@keyframes fadeIn {
from { opacity: 0; transform: translateY(20px); }
to { opacity: 1; transform: translateY(0); }
}

.animated {
animation: fadeIn 1s ease-out;
}

        /* Particle Background */

.particles {
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
z-index: -1;
pointer-events: none;
}

.particle {
position: absolute;
border-radius: 50%;
background: rgba(0, 247, 255, 0.5);
animation: float-particle 15s infinite linear;
}

@keyframes float-particle {
0% {
transform: translateY(0) translateX(0);
opacity: 0;
}
10% {
opacity: 1;
}
90% {
opacity: 1;
}
100% {
transform: translateY(-100vh) translateX(100px);
opacity: 0;
}
}

        /* Responsive Design */

@media (max-width: 768px) {
.header h1 {
font-size: 2.2rem;
}

.header h2 {
font-size: 1.2rem;
}

.skills-grid {
grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
}

.stats-grid {
grid-template-columns: 1fr;
}
}
</style>

</head>
<body>
    <div class="particles" id="particles"></div>
    
<div class="container">
        <header class="header animated">
            <div class="profile-pic">
                <img src="https://avatars.githubusercontent.com/u/583231?v=4" alt="Sandeep Bist">
            </div>
            <h1>Sandeep Bist</h1>
            <h2>🚀 Full-Stack Developer | Creative Builder | Tech Explorer</h2>
            
<div class="typing-container">
                <p id="typing-text"></p>
            </div>
 </header>
        
<section class="section animated">
            <h2><i class="fas fa-user"></i> About Me</h2>
            <p>I'm a passionate full-stack developer who loves creating innovative solutions and beautiful user experiences. With expertise in modern web technologies, I enjoy turning complex problems into simple, elegant solutions.</p>
            
<div class="about-details">
                <p><i class="fas fa-code"></i> <strong>Currently working with:</strong> React, Next.js, Node.js, TypeScript</p>
                <p><i class="fas fa-graduation-cap"></i> <strong>Learning:</strong> Advanced backend architectures, AI integration</p>
                <p><i class="fas fa-rocket"></i> <strong>Goals:</strong> Contribute to open source, build impactful products</p>
                <p><i class="fas fa-lightbulb"></i> <strong>Fun fact:</strong> I can solve a Rubik's cube in under 2 minutes!</p>
            </div>
        </section>
        
<section class="section animated">
            <h2><i class="fas fa-laptop-code"></i> Tech Stack</h2>
            
<h3>Frontend</h3>
            <div class="skills-grid">
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" alt="React">
                    <span>React</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg" alt="Next.js">
                    <span>Next.js</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" alt="TypeScript">
                    <span>TypeScript</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" alt="JavaScript">
                    <span>JavaScript</span>
                </div>
            </div>
            
<h3>Backend</h3>
            <div class="skills-grid">
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" alt="Node.js">
                    <span>Node.js</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/express/express-original.svg" alt="Express">
                    <span>Express</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" alt="PostgreSQL">
                    <span>PostgreSQL</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" alt="MongoDB">
                    <span>MongoDB</span>
                </div>
            </div>
            
<h3>Tools & Others</h3>
            <div class="skills-grid">
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" alt="Git">
                    <span>Git</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" alt="Docker">
                    <span>Docker</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/aws/aws-original.svg" alt="AWS">
                    <span>AWS</span>
                </div>
                <div class="skill-item">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg" alt="Figma">
                    <span>Figma</span>
                </div>
            </div>
        </section>
        
<section class="section animated">
            <h2><i class="fas fa-chart-line"></i> GitHub Stats</h2>
            
<div class="stats-grid">
                <div class="stat-card">
                    <h3>Commit Streak</h3>
                    <p>🔥 125 days</p>
                </div>
                <div class="stat-card">
                    <h3>Repositories</h3>
                    <p>📦 42</p>
                </div>
                <div class="stat-card">
                    <h3>Contributions</h3>
                    <p>⭐ 1.2k this year</p>
                </div>
                <div class="stat-card">
                    <h3>Followers</h3>
                    <p>👥 256</p>
                </div>
            </div>
            
<div class="stats-grid">
                <div class="stat-card">
                    <h3>Most Used Languages</h3>
                    <p>JavaScript: 45%</p>
                    <p>TypeScript: 35%</p>
                    <p>Python: 15%</p>
                    <p>Other: 5%</p>
                </div>
            </div>
        </section>
        
<section class="section animated">
            <h2><i class="fas fa-trophy"></i> Achievements</h2>
            
<div class="skills-grid">
                <div class="skill-item">
                    <i class="fas fa-code-branch fa-2x"></i>
                    <span>Hackathon Winner</span>
                </div>
                <div class="skill-item">
                    <i class="fas fa-star fa-2x"></i>
                    <span>GitHub Star</span>
                </div>
                <div class="skill-item">
                    <i class="fas fa-medal fa-2x"></i>
                    <span>Open Source</span>
                </div>
                <div class="skill-item">
                    <i class="fas fa-fire fa-2x"></i>
                    <span>Quick Deployer</span>
                </div>
            </div>
        </section>
        
<section class="section animated">
            <h2><i class="fas fa-quote-left"></i> Developer Quote</h2>
            <blockquote>
                <p>"First, solve the problem. Then, write the code."</p>
                <footer>— John Johnson</footer>
            </blockquote>
        </section>
        
<section class="section animated">
            <h2><i class="fas fa-calendar-alt"></i> Contribution Graph</h2>
            <div class="contribution-graph">
                <!-- This would be generated by GitHub, but we'll simulate it -->
                <div style="background: #1c1c1c; padding: 20px; border-radius: 10px; text-align: center;">
                    <p>GitHub Contribution Graph Would Appear Here</p>
                    <div style="display: flex; flex-wrap: wrap; justify-content: center; margin-top: 15px;">
                        <div style="width: 15px; height: 15px; background: #00ff95; margin: 2px; border-radius: 2px;"></div>
                        <div style="width: 15px; height: 15px; background: #00d97e; margin: 2px; border-radius: 2px;"></div>
                        <div style="width: 15px; height: 15px; background: #00b367; margin: 2px; border-radius: 2px;"></div>
                        <!-- More squares would be here -->
                    </div>
                </div>
            </div>
        </section>
        
<section class="section animated">
            <h2><i class="fas fa-hand-wave"></i> Connect With Me</h2>
            
<div class="social-links">
                <a href="https://github.com/sandeepbist" class="social-link">
                    <i class="fab fa-github"></i>
                </a>
                <a href="https://linkedin.com/in/sandeep-bist" class="social-link">
                    <i class="fab fa-linkedin-in"></i>
                </a>
                <a href="https://twitter.com/sandeepbist" class="social-link">
                    <i class="fab fa-twitter"></i>
                </a>
                <a href="mailto:sandeepbist.dev@gmail.com" class="social-link">
                    <i class="fas fa-envelope"></i>
                </a>
                <a href="https://portfolio.com" class="social-link">
                    <i class="fas fa-globe"></i>
                </a>
            </div>
        </section>
    </div>
    
<script>
        // Typing animation
        const texts = [
            "Turning Ideas into Code",
            "Full-Stack Developer",
            "React Native | Next.js | TypeScript",
            "Always Learning 🚀",
            "Building Cool Things!"
        ];
        
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;
        
        function type() {
            const currentText = texts[textIndex];
            const typingElement = document.getElementById('typing-text');
            
            if (isDeleting) {
                typingElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                typingSpeed = 50;
            } else {
                typingElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                typingSpeed = 100;
            }
            
            if (!isDeleting && charIndex === currentText.length) {
                isDeleting = true;
                typingSpeed = 1000;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                typingSpeed = 500;
            }
            
            setTimeout(type, typingSpeed);
        }
        
        // Create particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 50;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                
                const size = Math.random() * 5 + 2;
                const posX = Math.random() * 100;
                const delay = Math.random() * 15;
                
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${posX}vw`;
                particle.style.bottom = `-10px`;
                particle.style.animationDelay = `${delay}s`;
                
                particlesContainer.appendChild(particle);
            }
        }
        
        // Initialize animations
        document.addEventListener('DOMContentLoaded', function() {
            type();
            createParticles();
            
            // Add animation on scroll
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animated');
                    }
                });
            }, { threshold: 0.1 });
            
            document.querySelectorAll('.section').forEach(section => {
                observer.observe(section);
            });
        });
    </script>
</body>
</html>
