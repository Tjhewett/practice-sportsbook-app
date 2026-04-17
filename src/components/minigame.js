import React, { useEffect, useRef, useState } from 'react';
import '../styles/minigame.css';

const MiniGame = () => {
    const canvasRef = useRef(null);
    const [score, setScore] = useState(0);
    const [gameActive, setGameActive] = useState(false);
    const [userCurrency, setUserCurrency] = useState(0);
    const [footballs, setFootballs] = useState([]);
    const [player, setPlayer] = useState({
        x: 600, // Canvas width / 2 initially, adjust if canvas size changes
        y: 500, // Canvas height - 100, adjust if canvas size changes
        width: 80,
        height: 100,
        speed: 0.08,
        dx: 0
    });

    // Fetch user's currency and game settings from API
    useEffect(() => {
        fetchUserCurrency();

        const handleKeyDown = (e) => {
            if (e.key === 'ArrowRight' || e.key === 'd') {
                setPlayer(prevPlayer => ({ ...prevPlayer, dx: prevPlayer.speed }));
            } else if (e.key === 'ArrowLeft' || e.key === 'a') {
                setPlayer(prevPlayer => ({ ...prevPlayer, dx: -prevPlayer.speed }));
            }
        };

        const handleKeyUp = (e) => {
            if (['ArrowRight', 'ArrowLeft', 'd', 'a'].includes(e.key)) {
                setPlayer(prevPlayer => ({ ...prevPlayer, dx: 0 }));
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('keyup', handleKeyUp);
        };
    }, []);

    useEffect(() => {
        if (!gameActive) return;

        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        let animationFrameId;

        const render = () => {
            updateGame(context);
            animationFrameId = window.requestAnimationFrame(render);
        };

        render();
        return () => {
            window.cancelAnimationFrame(animationFrameId);
        };
    }, [gameActive, footballs, player]);

    const fetchUserCurrency = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/account', {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            });
            const data = await response.json();
            setUserCurrency(data.currency);
        } catch (error) {
            console.error('Failed to fetch user currency:', error);
        }
    };

    const lastRenderTime = useRef(Date.now());
    const updateGame = (ctx) => {
        const currentTime = Date.now();
        const deltaTime = (currentTime - lastRenderTime.current) / 1000; 
        lastRenderTime.current = currentTime;
    
        clearCanvas(ctx);
        handleFootballs(ctx, deltaTime);
        drawPlayer(ctx);
        updatePlayerPosition(deltaTime);
    };

    const handleFootballs = (ctx) => {
        // Add new football
        if (Math.random() < 0.0005) {
            const newFootball = {
                x: Math.random() * canvasRef.current.width,
                y: 0,
                size: 50,
                speed: 0.06
            };
            setFootballs(prevFootballs => [...prevFootballs, newFootball]);
        }

        // Move footballs
        setFootballs(prevFootballs => prevFootballs.map(fb => ({ ...fb, y: fb.y + fb.speed })));

        // Collision detection
        footballs.forEach((football, index) => {
            if (footballCollision(football)) {
                setScore(prevScore => prevScore + 10);
                setFootballs(prevFootballs => prevFootballs.filter((_, i) => i !== index));
            }
        });

        // Draw footballs
        footballs.forEach(fb => {
            ctx.fillStyle = 'gray';
            ctx.beginPath();
            ctx.arc(fb.x, fb.y, fb.size, 0, Math.PI * 2);
            ctx.fill();
        });
    };

    const footballCollision = (football) => {
        return (
            football.x < player.x + player.width &&
            football.x + football.size > player.x &&
            football.y < player.y + player.height &&
            football.y + football.size > player.y
        );
    };

    const drawPlayer = (ctx) => {
        ctx.fillStyle = 'blue';
        ctx.fillRect(player.x, player.y, player.width, player.height);
    };

    const updatePlayerPosition = () => {
        setPlayer(prevPlayer => {
            let newX = prevPlayer.x + prevPlayer.dx;
            newX = Math.max(0, Math.min(newX, canvasRef.current.width - prevPlayer.width));
            return { ...prevPlayer, x: newX };
        });
    };


    const clearCanvas = (ctx) => {
        ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    };

    const startGame = () => {
        setGameActive(true);
        setFootballs([]);
        setScore(0);
    };

    const endGame = () => {
        setGameActive(false);
        sendScoreToBackend(score);
    };

    const sendScoreToBackend = async (finalScore) => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/update_currency', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ score: finalScore })
            });
            if (!response.ok) {
                throw new Error('Failed to update currency');
            }
            const data = await response.json();
            setUserCurrency(data.newCurrency); // Update user currency
        } catch (error) {
            console.error('Error updating currency:', error);
        }
    };    

    return (
        <div className="mini-game-container">
            <h1>Top-Down Mini Game</h1>
            <h4>A&D keys OR Left&Right arrows to move</h4>
            <button onClick={startGame}>Start Game</button>
            {gameActive && <button onClick={endGame}>End Game</button>}
            <canvas ref={canvasRef} width={1200} height={600} />
            <p>Score: {score}</p>
            <p>Currency: ${userCurrency}</p>
        </div>
    );
};

export default MiniGame;
