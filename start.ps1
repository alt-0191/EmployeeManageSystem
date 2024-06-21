#激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动前端服务
cd frontend
npm install
npm start

# 启动后端服务
cd ../backend
python app.py
cd ..

