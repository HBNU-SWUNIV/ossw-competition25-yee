<template>
  <div class="welcome-section">
    <div class="welcome-card">
      <h2>{{ msg }}</h2>
      <p class="description">
        왼쪽 상단의 햄버거 메뉴를 클릭하여 다양한 기능을 이용하세요.
      </p>
      
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <h3>총 예산</h3>
            <p>₩10,000,000</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <h3>이번 달 지출</h3>
            <p>₩3,250,000</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <h3>절약률</h3>
            <p>67.5%</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🏢</div>
          <div class="stat-info">
            <h3>활성 부서</h3>
            <p>12개</p>
          </div>
        </div>
      </div>
      
      <div class="action-buttons">
        <button class="primary-btn">새 예산 등록</button>
        <button class="secondary-btn">지출 추가</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<style scoped>
.welcome-section {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.welcome-card h2 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 1rem;
  text-align: center;
}

.description {
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 2.5rem;
  margin-right: 1rem;
}

.stat-info h3 {
  color: #2c3e50;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.stat-info p {
  color: #1976d2;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.primary-btn, .secondary-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn {
  background: #1976d2;
  color: white;
}

.primary-btn:hover {
  background: #1565c0;
  transform: translateY(-1px);
}

.secondary-btn {
  background: transparent;
  color: #1976d2;
  border: 2px solid #1976d2;
}

.secondary-btn:hover {
  background: #1976d2;
  color: white;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .welcome-card {
    padding: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .stat-card {
    padding: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .primary-btn, .secondary-btn {
    width: 100%;
  }
}
</style>