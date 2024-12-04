# AI HR Agent

一个基于AI的自动化HR系统，用于简历筛选和面试管理。


## 功能特性

- 自动简历解析和分析
- 智能评分系统
- 教育背景分析
- 工作经验评估
- 技能匹配度分析
- 求职信评估（可选）

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- SpaCy
- Transformers
- Pydantic

### 前端
- React
- TypeScript
- Ant Design
- Axios

## 安装说明

1. 克隆仓库
```
git clone https://github.com/miofuku/alltimehr.git
cd alltimehr
```

2. 安装后端依赖
```
cd backend
python -m venv venv
source venv/bin/activate # Windows使用: venv\Scripts\activate
pip install -r requirements.txt
```

3. 安装前端依赖
```
cd frontend
npm install
```

## 运行项目

1. 启动后端服务
```
cd backend
uvicorn main:app --reload
```

2. 启动前端开发服务器
```
cd frontend
npm start
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看API文档。

## 配置说明

1. 后端配置在 `backend/app/config.py`
2. 前端配置在 `frontend/src/config.ts`

## 许可证

MIT License