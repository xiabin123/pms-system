"""
数据库模型 - PMS 生产管理系统
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, comment="用户名")
    password_hash = Column(String(200), comment="密码哈希")
    role = Column(String(50), default="operator", comment="角色")
    real_name = Column(String(50), comment="真实姓名")
    department = Column(String(50), comment="部门/班组")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.now)

class Role(Base):
    """角色表"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, comment="角色名称")
    code = Column(String(50), unique=True, comment="角色代码")
    permissions = Column(Text, comment="权限配置 (JSON)")
    description = Column(String(200), comment="描述")
    menu_access = Column(Text, comment="可访问菜单 (JSON)")
    created_at = Column(DateTime, default=datetime.now)

class ProductModel(Base):
    """产品型号表"""
    __tablename__ = "product_models"
    
    id = Column(Integer, primary_key=True, index=True)
    model_number = Column(String(100), unique=True, comment="型号")
    name = Column(String(200), comment="产品名称")
    category = Column(String(50), comment="产品类别")
    process_route = Column(Text, comment="工艺路线 (JSON)")
    created_at = Column(DateTime, default=datetime.now)

class Process(Base):
    """工序表"""
    __tablename__ = "processes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, comment="工序代码")
    name = Column(String(100), comment="工序名称")
    description = Column(Text, comment="工序描述")
    standard_qty = Column(Integer, default=0, comment="标准日产量")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.now)

class WorkOrder(Base):
    """工单表"""
    __tablename__ = "work_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, comment="工单号")
    category = Column(String(50), index=True, comment="工单类别")
    product_model = Column(String(100), comment="产品型号/名称编码")
    product_name = Column(String(200), comment="产品名称")
    quantity = Column(Integer, comment="数量")
    status = Column(String(20), default="待下发", comment="状态：待下发/已下发/生产中/已完成/延误")
    priority = Column(String(10), default="普通", comment="优先级：紧急/普通")
    
    plan_start = Column(DateTime, comment="计划开始")
    plan_end = Column(DateTime, comment="计划结束")
    actual_start = Column(DateTime, comment="实际开始")
    actual_end = Column(DateTime, comment="实际结束")
    
    parent_order_id = Column(Integer, ForeignKey("work_orders.id"), comment="关联父工单 ID")
    source_type = Column(String(50), comment="来源类型：手动创建/流转生成")
    
    remark = Column(Text, comment="备注")
    created_by = Column(String(50), comment="创建人")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class WorkOrderStep(Base):
    """工单步骤表"""
    __tablename__ = "work_order_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), index=True, comment="工单 ID")
    step_number = Column(Integer, comment="步骤序号")
    step_name = Column(String(100), comment="步骤名称")
    step_content = Column(Text, comment="步骤内容描述")
    standard_qty = Column(Integer, comment="标准日产量")
    planned_qty = Column(Integer, comment="计划数量")
    
    status = Column(String(20), default="待开始", comment="状态：待开始/进行中/已完成/已跳过")
    actual_qty = Column(Integer, default=0, comment="实际完成数量")
    
    start_time = Column(DateTime, comment="步骤开始时间")
    end_time = Column(DateTime, comment="步骤完成时间")
    
    assigned_to = Column(String(200), comment="分配给 (班组/人员)")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.now)

class WorkOrderStepRecord(Base):
    """工单步骤登记记录表"""
    __tablename__ = "work_order_step_records"
    
    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), index=True, comment="工单 ID")
    step_id = Column(Integer, ForeignKey("work_order_steps.id"), comment="步骤 ID")
    
    operator_id = Column(Integer, ForeignKey("users.id"), comment="操作员 ID")
    operator_name = Column(String(50), comment="操作员姓名")
    
    work_hours = Column(Float, default=0, comment="工时 (小时)")
    completed_qty = Column(Integer, default=0, comment="完成数量")
    work_ratio = Column(Float, default=1.0, comment="工作量比例 (默认 1.0 均分)")
    
    record_time = Column(DateTime, default=datetime.now, comment="登记时间")
    remark = Column(Text, comment="备注")

class Material(Base):
    """物料表"""
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, comment="物料编号")
    name = Column(String(100), comment="品名")
    specification = Column(String(200), comment="型号规格")
    category = Column(String(50), comment="类别")
    stock_qty = Column(Integer, default=0, comment="库存数量")
    created_at = Column(DateTime, default=datetime.now)

class DeliveryOrder(Base):
    """发货单表"""
    __tablename__ = "delivery_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, comment="发货单号")
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), comment="关联工单 ID")
    
    recipient_name = Column(String(100), comment="收货人")
    recipient_phone = Column(String(20), comment="联系电话")
    recipient_address = Column(String(500), comment="收货地址")
    
    package_count = Column(Integer, default=0, comment="箱数")
    logistics_company = Column(String(100), comment="物流公司")
    logistics_number = Column(String(100), comment="物流单号")
    
    status = Column(String(20), default="待发货", comment="状态")
    ship_time = Column(DateTime, comment="发货时间")
    
    created_at = Column(DateTime, default=datetime.now)

class RepairOrder(Base):
    """维修/售后单表"""
    __tablename__ = "repair_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, comment="维修单号")
    type = Column(String(20), comment="类型：维修/售后")
    
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), comment="关联工单 ID")
    product_model = Column(String(100), comment="产品型号")
    customer_name = Column(String(100), comment="客户名称")
    customer_contact = Column(String(100), comment="客户联系方式")
    
    issue_description = Column(Text, comment="问题描述")
    solution = Column(Text, comment="处理方案")
    
    status = Column(String(20), default="待处理", comment="状态")
    handler = Column(String(50), comment="处理人")
    
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, comment="完成时间")
