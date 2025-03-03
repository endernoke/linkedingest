import { useState, useEffect } from 'react';

function useCountdown(targetDate) {
  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft(targetDate));

  function calculateTimeLeft(targetDate) {
    const difference = new Date(targetDate) - new Date();
    
    if (difference <= 0) {
      return null;
    }

    return {
      minutes: Math.floor((difference / 1000 / 60) % 60),
      seconds: Math.floor((difference / 1000) % 60)
    };
  }

  useEffect(() => {
    if (!targetDate) return;

    const timer = setInterval(() => {
      const calculated = calculateTimeLeft(targetDate);
      setTimeLeft(calculated);
      
      if (!calculated) {
        clearInterval(timer);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [targetDate]);

  return timeLeft;
}

export default useCountdown;