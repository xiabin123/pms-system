"""
PMS 生产管理系统 - 后端 API
"""
from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
import models
from database import engine, get_db
import json

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PMS 生产管理系统",
    description="生产管理系统 API - 工单管理/角色权限/流程流转",
    version="2.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== Pydantic Models ==============

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    real_name: str
    role: str
    department: str
    class Config:
        from_attributes = True

class WorkOrderStepCreate(BaseModel):
    step_number: int
    step_name: str
    step_content: str = ""
    standard_qty: int = 0
    planned_qty: int = 0

class WorkOrderCreate(BaseModel):
    order_number: str
    category: str
    product_model: str
    product_name: str = ""
    quantity: int
    priority: str = "普通"
    plan_start: Optional[str] = None
    plan_end: Optional[str] = None
    steps: List[WorkOrderStepCreate] = []
    remark: str = ""

class WorkOrderStepRecordCreate(BaseModel):
    step_id: int
    operator_id: int
    operator_name: str
    work_hours: float = 0
    completed_qty: int = 0
    work_ratio: float = 1.0
    remark: str = ""

class WorkOrderUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    remark: Optional[str] = None

class WorkOrderResponse(BaseModel):
    id: int
    order_number: str
    category: str
    product_model: str
    product_name: Optional[str] = ""
    quantity: int
    status: str
    priority: str
    plan_start: Optional[datetime] = None
    plan_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    parent_order_id: Optional[int] = None
    source_type: Optional[str] = "手动创建"
    created_by: Optional[str] = ""
    created_at: datetime
    class Config:
        from_attributes = True

# ============== Mock Data ==============

MOCK_USERS = [
    {"id": 1, "username": "admin", "password": "admin123", "real_name": "系统管理员", "role": "admin", "department": "管理部"},
    {"id": 2, "username": "plan001", "password": "123456", "real_name": "张三", "role": "planner", "department": "计划部"},
    {"id": 3, "username": "hb001", "password": "123456", "real_name": "李四", "role": "hanjie", "department": "焊接组"},
    {"id": 4, "username": "zp001", "password": "123456", "real_name": "王五", "role": "zhuangpei", "department": "装配组"},
    {"id": 5, "username": "cs001", "password": "123456", "real_name": "赵六", "role": "ceshi", "department": "调试组"},
    {"id": 6, "username": "lh001", "password": "123456", "real_name": "钱七", "role": "laohua", "department": "老化组"},
    {"id": 7, "username": "jy001", "password": "123456", "real_name": "孙八", "role": "jianyan", "department": "检验组"},
    {"id": 8, "username": "bz001", "password": "123456", "real_name": "周九", "role": "baozhuang", "department": "包装组"},
    {"id": 9, "username": "fh001", "password": "123456", "real_name": "吴十", "role": "fahuo", "department": "发货组"},
    {"id": 10, "username": "sh001", "password": "123456", "real_name": "郑一", "role": "shouhou", "department": "售后部"},
]

ROLES = {
    "admin": {"name": "系统管理员", "menus": ["all"], "can_approve": True},
    "planner": {"name": "计划员", "menus": ["create_order", "assign_order", "work_orders", "reports"], "can_create": True},
    "hanjie": {"name": "焊接工", "menus": ["work_orders", "step_register"], "can_register": True},
    "zhuangpei": {"name": "装配工", "menus": ["work_orders", "step_register"], "can_register": True},
    "ceshi": {"name": "调试工", "menus": ["work_orders", "step_register"], "can_register": True},
    "laohua": {"name": "老化工", "menus": ["work_orders", "step_register"], "can_register": True},
    "jianyan": {"name": "检验员", "menus": ["work_orders", "step_register", "quality"], "can_register": True, "can_inspect": True},
    "baozhuang": {"name": "包装工", "menus": ["work_orders", "step_register"], "can_register": True},
    "fahuo": {"name": "发货员", "menus": ["work_orders", "delivery"], "can_ship": True},
    "shouhou": {"name": "售后员", "menus": ["work_orders", "repair"], "can_repair": True},
}

WORK_ORDER_CATEGORIES = {
    "线路板工单": ["补焊 1", "补焊 2", "补焊 3"],
    "半成品工单": ["补焊", "装配", "调试 1", "调试 2", "老化"],
    "成品工单": ["补焊", "装配", "调试 1", "调试 2", "老化", "送检", "检验 1", "检验 2"],
    "检验工单": ["送检", "检验 1", "检验 2"],
    "发货工单": ["核对", "装箱", "物流登记"],
    "维修工单": ["维修登记", "维修处理", "维修完成"],
    "售后工单": ["售后登记", "售后处理", "售后完成"],
}

# ============== API Routes ==============

@app.get("/")
def root():
    return {"message": "PMS 生产管理系统 API v2.0", "docs": "/docs"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now()}

# ----- 认证 -----

@app.post("/api/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    
    if not user:
        # 检查 mock 用户
        for mock in MOCK_USERS:
            if mock["username"] == request.username and mock["password"] == request.password:
                return {
                    "token": f"mock-token-{mock['id']}",
                    "user": {"id": mock["id"], "username": mock["username"], "real_name": mock["real_name"], "role": mock["role"], "department": mock["department"]}
                }
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    if user.password_hash != request.password:  # 简化：直接比较
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    return {
        "token": f"token-{user.id}",
        "user": {"id": user.id, "username": user.username, "real_name": user.real_name, "role": user.role, "department": user.department}
    }

@app.get("/api/auth/me")
def get_current_user(db: Session = Depends(get_db)):
    users = db.query(models.User).limit(10).all()
    return [UserResponse.from_orm(u) for u in users] if users else MOCK_USERS[:10]

@app.get("/api/roles")
def get_roles():
    return [{"code": k, **v} for k, v in ROLES.items()]

@app.get("/api/menu/{role_code}")
def get_menu(role_code: str):
    role = ROLES.get(role_code, ROLES["operator"])
    return {"menus": role.get("menus", []), "permissions": role}

# ----- 工单管理 -----

@app.post("/api/work-orders", response_model=WorkOrderResponse)
def create_work_order(order: WorkOrderCreate, db: Session = Depends(get_db)):
    # 创建工单
    db_order = models.WorkOrder(
        order_number=order.order_number,
        category=order.category,
        product_model=order.product_model,
        product_name=order.product_name,
        quantity=order.quantity,
        priority=order.priority,
        status="待下发",
        plan_start=datetime.fromisoformat(order.plan_start) if order.plan_start else None,
        plan_end=datetime.fromisoformat(order.plan_end) if order.plan_end else None,
        remark=order.remark,
        created_by="admin",
        source_type="手动创建"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # 创建步骤
    if order.steps:
        for step_data in order.steps:
            db_step = models.WorkOrderStep(
                work_order_id=db_order.id,
                **step_data.model_dump()
            )
            db.add(db_step)
    db.commit()
    
    return WorkOrderResponse.from_orm(db_order)

@app.get("/api/work-orders")
def get_work_orders(
    category: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.WorkOrder)
    
    if category:
        query = query.filter(models.WorkOrder.category == category)
    if status:
        query = query.filter(models.WorkOrder.status == status)
    if keyword:
        query = query.filter(
            (models.WorkOrder.order_number.contains(keyword)) |
            (models.WorkOrder.product_model.contains(keyword))
        )
    
    total = query.count()
    orders = query.order_by(models.WorkOrder.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "data": [WorkOrderResponse.from_orm(o) for o in orders]}

@app.get("/api/work-orders/{order_id}")
def get_work_order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    steps = db.query(models.WorkOrderStep).filter(models.WorkOrderStep.work_order_id == order_id).all()
    records = db.query(models.WorkOrderStepRecord).filter(models.WorkOrderStepRecord.work_order_id == order_id).all()
    
    return {
        "order": WorkOrderResponse.from_orm(order),
        "steps": [{"id": s.id, "step_number": s.step_number, "step_name": s.step_name, "step_content": s.step_content, "status": s.status, "actual_qty": s.actual_qty, "planned_qty": s.planned_qty} for s in steps],
        "records": [{"id": r.id, "step_id": r.step_id, "operator_name": r.operator_name, "work_hours": r.work_hours, "completed_qty": r.completed_qty, "record_time": r.record_time} for r in records]
    }

@app.put("/api/work-orders/{order_id}")
def update_work_order(order_id: int, update: WorkOrderUpdate, db: Session = Depends(get_db)):
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    if update.status:
        order.status = update.status
        if update.status == "生产中" and not order.actual_start:
            order.actual_start = datetime.now()
        if update.status == "已完成":
            order.actual_end = datetime.now()
    if update.priority:
        order.priority = update.priority
    if update.remark:
        order.remark = update.remark
    
    db.commit()
    return {"message": "更新成功"}

@app.post("/api/work-orders/{order_id}/assign")
def assign_work_order(order_id: int, db: Session = Depends(get_db)):
    """下发工单"""
    order = db.query(models.WorkOrder).filter(models.WorkOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    order.status = "已下发"
    db.commit()
    return {"message": "工单已下发"}

@app.post("/api/work-orders/{order_id}/steps/{step_id}/record")
def register_step_record(order_id: int, step_id: int, record: WorkOrderStepRecordCreate, db: Session = Depends(get_db)):
    """步骤登记"""
    step = db.query(models.WorkOrderStep).filter(
        models.WorkOrderStep.id == step_id,
        models.WorkOrderStep.work_order_id == order_id
    ).first()
    if not step:
        raise HTTPException(status_code=404, detail="步骤不存在")
    
    # 创建登记记录
    db_record = models.WorkOrderStepRecord(
        work_order_id=order_id,
        step_id=step_id,
        **record.model_dump()
    )
    db.add(db_record)
    
    # 更新步骤状态
    step.actual_qty = (step.actual_qty or 0) + record.completed_qty
    if step.actual_qty >= step.planned_qty:
        step.status = "已完成"
        step.end_time = datetime.now()
    elif step.status == "待开始":
        step.status = "进行中"
        step.start_time = datetime.now()
    
    # 检查工单是否完成
    all_steps = db.query(models.WorkOrderStep).filter(models.WorkOrderStep.work_order_id == order_id).all()
    if all(s.status == "已完成" for s in all_steps):
        order = db.query(models.WorkOrder).filter(models.WorkOrder.id == order_id).first()
        order.status = "已完成"
        order.actual_end = datetime.now()
    
    db.commit()
    return {"message": "登记成功"}

@app.get("/api/work-order-categories")
def get_work_order_categories():
    return [{"name": k, "steps": v} for k, v in WORK_ORDER_CATEGORIES.items()]

# ----- 统计 -----

@app.get("/api/stats/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(models.WorkOrder).count()
    completed = db.query(models.WorkOrder).filter(models.WorkOrder.status == "已完成").count()
    processing = db.query(models.WorkOrder).filter(models.WorkOrder.status == "生产中").count()
    pending = db.query(models.WorkOrder).filter(models.WorkOrder.status == "待下发").count()
    delayed = db.query(models.WorkOrder).filter(models.WorkOrder.status == "延误").count()
    
    return {
        "total": total,
        "completed": completed,
        "processing": processing,
        "pending": pending,
        "delayed": delayed
    }

# ----- 物料 -----

@app.get("/api/materials")
def get_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materials = db.query(models.Material).offset(skip).limit(limit).all()
    total = db.query(models.Material).count()
    return {"total": total, "data": [{"id": m.id, "code": m.code, "name": m.name, "specification": m.specification} for m in materials]}

@app.post("/api/materials/import")
def import_materials(db: Session = Depends(get_db)):
    import pandas as pd
    material_file = r"D:\qt\物料编号.xlsx"
    df = pd.read_excel(material_file)
    
    count = 0
    for _, row in df.iterrows():
        material = models.Material(
            code=str(row.iloc[0]),
            name=str(row.iloc[1]) if len(row) > 1 else "",
            specification=str(row.iloc[2]) if len(row) > 2 else ""
        )
        db.add(material)
        count += 1
        if count >= 500:
            break
    
    db.commit()
    return {"message": f"成功导入 {count} 条物料数据"}

# ----- 初始化 -----

@app.post("/api/init/mock-data")
def init_mock_data(db: Session = Depends(get_db)):
    """初始化模拟数据"""
    # 创建用户
    for mock in MOCK_USERS:
        user = models.User(
            username=mock["username"],
            password_hash=mock["password"],
            real_name=mock["real_name"],
            role=mock["role"],
            department=mock["department"]
        )
        db.add(user)
    
    # 创建示例工单
    sample_orders = [
        {"order_number": "WO20250115001", "category": "线路板工单", "product_model": "ZEF650(4P)_Main", "quantity": 500, "status": "已完成"},
        {"order_number": "WO20250115002", "category": "半成品工单", "product_model": "ZEF650(4P)", "quantity": 300, "status": "生产中"},
        {"order_number": "WO20250115003", "category": "成品工单", "product_model": "ZEF650-4PC40", "quantity": 200, "status": "待下发"},
        {"order_number": "WO20250115004", "category": "检验工单", "product_model": "ZEF650-4PC40", "quantity": 200, "status": "已完成"},
        {"order_number": "WO20250115005", "category": "发货工单", "product_model": "ZEF650-4PC40", "quantity": 200, "status": "已完成"},
    ]
    
    for so in sample_orders:
        order = models.WorkOrder(**so, created_by="admin")
        db.add(order)
        
        # 添加步骤
        category = so["category"]
        steps = WORK_ORDER_CATEGORIES.get(category, ["步骤 1"])
        for i, step_name in enumerate(steps):
            db_step = models.WorkOrderStep(
                work_order_id=order.id + 1 if order.id else 1,
                step_number=i+1,
                step_name=step_name,
                planned_qty=so["quantity"]
            )
            db.add(db_step)
    
    db.commit()
    return {"message": "初始化完成"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
