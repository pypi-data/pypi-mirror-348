"""Test cases for JSDC Loader."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict, Set, Any, Union, Tuple
import tempfile
import os
import unittest
import datetime
import uuid
import json
from decimal import Decimal

from pydantic import BaseModel

from .loader import jsdc_load, jsdc_loads
from .dumper import jsdc_dump, jsdc_dumps

class TestJSDCLoader(unittest.TestCase):
    """Test suite for JSDC Loader."""
    
    def setUp(self):
        """Set up the test environment."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        
    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
    
    def test_basic_serialization(self):
        """Test basic dataclass serialization/deserialization."""
        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
            user: str = 'root'
            password: str = 'password'
            ips: List[str] = field(default_factory=lambda: ['127.0.0.1'])
            primary_user: Optional[str] = field(default_factory=lambda: None)
        
        db = DatabaseConfig()
        jsdc_dump(db, self.temp_path)
        loaded_db = jsdc_load(self.temp_path, DatabaseConfig)
        
        self.assertEqual(db.host, loaded_db.host)
        self.assertEqual(db.port, loaded_db.port)
        self.assertEqual(db.ips, loaded_db.ips)
    
    def test_enum_serialization(self):
        """Test enum serialization/deserialization."""
        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass 
        class UserConfig:
            name: str = 'John Doe'
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ['read'])
        
        user = UserConfig()
        jsdc_dump(user, self.temp_path)
        loaded_user = jsdc_load(self.temp_path, UserConfig)
        
        self.assertEqual(user.name, loaded_user.name)
        self.assertEqual(user.user_type, loaded_user.user_type)
    
    def test_nested_dataclasses(self):
        """Test nested dataclasses serialization/deserialization."""
        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass 
        class UserConfig:
            name: str = 'John Doe'
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ['read'])

        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
            user: str = 'root'
            password: str = 'password'
            ips: List[str] = field(default_factory=lambda: ['127.0.0.1'])
            primary_user: Optional[str] = field(default_factory=lambda: None)

        @dataclass
        class AppConfig:
            user: UserConfig = field(default_factory=lambda: UserConfig())
            database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
            version: str = '1.0.0'
            debug: bool = False
            settings: Dict[str, str] = field(default_factory=lambda: {'theme': 'dark'})
        
        app = AppConfig()
        app.user.roles.append('write')
        app.database.ips.extend(['192.168.1.1', '10.0.0.1'])
        app.settings['language'] = 'en'
        
        jsdc_dump(app, self.temp_path)
        loaded_app = jsdc_load(self.temp_path, AppConfig)
        
        self.assertEqual(loaded_app.user.roles, ['read', 'write'])
        self.assertEqual(loaded_app.database.ips, ['127.0.0.1', '192.168.1.1', '10.0.0.1'])
        self.assertEqual(loaded_app.settings, {'theme': 'dark', 'language': 'en'})
    
    def test_pydantic_models(self):
        """Test Pydantic models serialization/deserialization."""
        class ServerConfig(BaseModel):
            name: str = "main"
            port: int = 8080
            ssl: bool = True
            headers: Dict[str, str] = {"Content-Type": "application/json"}

        class ApiConfig(BaseModel):
            servers: List[ServerConfig] = []
            timeout: int = 30
            retries: int = 3
        
        api_config = ApiConfig()
        api_config.servers.append(ServerConfig(name="backup", port=8081))
        api_config.servers.append(ServerConfig(name="dev", port=8082, ssl=False))
        
        jsdc_dump(api_config, self.temp_path)
        loaded_api = jsdc_load(self.temp_path, ApiConfig)
        
        self.assertEqual(len(loaded_api.servers), 2)
        self.assertEqual(loaded_api.servers[0].name, "backup")
        self.assertEqual(loaded_api.servers[1].port, 8082)
        self.assertFalse(loaded_api.servers[1].ssl)
    
    def test_hashable_model_set(self):
        """Test serialization/deserialization of hashable dataclasses with set."""
        # 杂鱼♡～为了让Model可哈希，本喵决定添加__hash__和__eq__方法喵～ 
        @dataclass(frozen=True)  # 让这个数据类不可变，以便可以哈希
        class Model:
            base_url: str = ""
            api_key: str = ""
            model: str = ""

            def __hash__(self):
                return hash((self.base_url, self.api_key, self.model))  # 使用元组的哈希值

            def __eq__(self, other):
                if not isinstance(other, Model):
                    return NotImplemented
                return (self.base_url, self.api_key, self.model) == (other.base_url, other.api_key, other.model)  # 比较内容

        @dataclass
        class ModelList:
            models: Set[Model] = field(default_factory=lambda: set()) 
            
        # 创建测试数据
        model1 = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
        model2 = Model(base_url="https://api2.example.com", api_key="key2", model="gpt-3.5")
        model3 = Model(base_url="https://api3.example.com", api_key="key3", model="llama-3")
        
        model_list = ModelList()
        model_list.models.add(model1)
        model_list.models.add(model2)
        model_list.models.add(model3)
        
        # 测试相同模型的哈希值和相等性
        duplicate_model = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
        model_list.models.add(duplicate_model)  # 这个不应该增加集合的大小
        
        self.assertEqual(len(model_list.models), 3)  # 验证重复模型没有被添加
        self.assertEqual(hash(model1), hash(duplicate_model))  # 验证哈希函数工作正常
        self.assertEqual(model1, duplicate_model)  # 验证相等性比较工作正常
        
        # 序列化和反序列化
        jsdc_dump(model_list, self.temp_path)
        loaded_model_list = jsdc_load(self.temp_path, ModelList)
        
        # 验证集合大小
        self.assertEqual(len(loaded_model_list.models), 3)
        
        # 验证所有模型都被正确反序列化
        loaded_models = sorted(loaded_model_list.models, key=lambda m: m.base_url)
        original_models = sorted(model_list.models, key=lambda m: m.base_url)
        
        for i in range(len(original_models)):
            self.assertEqual(loaded_models[i].base_url, original_models[i].base_url)
            self.assertEqual(loaded_models[i].api_key, original_models[i].api_key)
            self.assertEqual(loaded_models[i].model, original_models[i].model)
        
        # 验证集合操作仍然正常工作
        new_model = Model(base_url="https://api4.example.com", api_key="key4", model="claude-3")
        loaded_model_list.models.add(new_model)
        self.assertEqual(len(loaded_model_list.models), 4)
        
        # 验证重复模型仍然不会被添加
        duplicate_model_again = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
        loaded_model_list.models.add(duplicate_model_again)
        self.assertEqual(len(loaded_model_list.models), 4)
    
    def test_error_handling(self):
        """Test error handling."""
        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
        
        # Test nonexistent file
        with self.assertRaises(FileNotFoundError):
            jsdc_load("nonexistent.json", DatabaseConfig)
        
        # Test empty input
        with self.assertRaises(ValueError):
            jsdc_loads("", DatabaseConfig)
        
        # Test invalid JSON
        with self.assertRaises(ValueError):
            jsdc_loads("{invalid json}", DatabaseConfig)
        
        # Test invalid indent
        with self.assertRaises(ValueError):
            jsdc_dump(DatabaseConfig(), self.temp_path, indent=-1)
            
    def test_complex_types(self):
        """Test serialization/deserialization of complex data types."""
        # 杂鱼♡～本喵要测试各种复杂类型了喵～准备好被本喵的测试震撼吧～
        @dataclass
        class ComplexConfig:
            created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())
            updated_at: Optional[datetime.datetime] = None
            expiry_date: Optional[datetime.date] = field(default_factory=lambda: datetime.date.today())
            session_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4())
            amount: Decimal = Decimal('10.50')
            time_delta: datetime.timedelta = datetime.timedelta(days=7)
            
        complex_obj = ComplexConfig()
        complex_obj.updated_at = datetime.datetime.now()
        
        jsdc_dump(complex_obj, self.temp_path)
        loaded_obj = jsdc_load(self.temp_path, ComplexConfig)
        
        self.assertEqual(complex_obj.created_at, loaded_obj.created_at)
        self.assertEqual(complex_obj.updated_at, loaded_obj.updated_at)
        self.assertEqual(complex_obj.expiry_date, loaded_obj.expiry_date)
        self.assertEqual(complex_obj.session_id, loaded_obj.session_id)
        self.assertEqual(complex_obj.amount, loaded_obj.amount)
        self.assertEqual(complex_obj.time_delta, loaded_obj.time_delta)
        
    def test_deeply_nested_structures(self):
        """Test serialization/deserialization of deeply nested structures."""
        # 杂鱼♡～嘻嘻～本喵要测试超级深的嵌套结构了喵～杂鱼会头晕的吧～
        @dataclass
        class Level3:
            name: str = "level3"
            value: int = 3
            
        @dataclass
        class Level2:
            name: str = "level2"
            value: int = 2
            level3_items: List[Level3] = field(default_factory=lambda: [Level3()])
            level3_dict: Dict[str, Level3] = field(default_factory=lambda: {"default": Level3()})
            
        @dataclass
        class Level1:
            name: str = "level1"
            value: int = 1
            level2_items: List[Level2] = field(default_factory=lambda: [Level2()])
            level2_dict: Dict[str, Level2] = field(default_factory=lambda: {"default": Level2()})
            
        @dataclass
        class RootConfig:
            name: str = "root"
            level1_items: List[Level1] = field(default_factory=lambda: [Level1()])
            level1_dict: Dict[str, Level1] = field(default_factory=lambda: {"default": Level1()})
            
        # 创建深度嵌套结构
        root = RootConfig()
        root.level1_items.append(Level1(name="custom_level1"))
        root.level1_dict["custom"] = Level1(name="custom_dict_level1")
        root.level1_dict["custom"].level2_items.append(Level2(name="custom_level2"))
        root.level1_dict["custom"].level2_items[0].level3_items.append(Level3(name="custom_level3", value=99))
        
        jsdc_dump(root, self.temp_path)
        loaded_root = jsdc_load(self.temp_path, RootConfig)
        
        # 验证深度嵌套的值
        self.assertEqual(loaded_root.level1_dict["custom"].level2_items[0].level3_items[1].name, "custom_level3")
        self.assertEqual(loaded_root.level1_dict["custom"].level2_items[0].level3_items[1].value, 99)
        
    def test_string_serialization(self):
        """Test string serialization/deserialization with jsdc_dumps and jsdc_loads."""
        # 杂鱼♡～本喵要测试字符串序列化了喵～这种基础功能都要本喵教你吗～
        @dataclass
        class Config:
            name: str = "test"
            values: List[int] = field(default_factory=lambda: [1, 2, 3])
            
        # 创建测试对象
        config = Config(name="string_test", values=[5, 6, 7, 8])
        
        # 序列化到字符串
        serialized_str = jsdc_dumps(config)
        self.assertIsInstance(serialized_str, str)
        
        # 从字符串反序列化
        loaded_config = jsdc_loads(serialized_str, Config)
        
        # 验证值
        self.assertEqual(config.name, loaded_config.name)
        self.assertEqual(config.values, loaded_config.values)
        
    def test_empty_collections(self):
        """Test serialization/deserialization of empty collections."""
        # 杂鱼♡～本喵来测试空集合的情况了喵～杂鱼肯定忘记处理这种情况了吧～
        @dataclass
        class EmptyCollections:
            empty_list: List[str] = field(default_factory=list)
            empty_dict: Dict[str, int] = field(default_factory=dict)
            empty_set: Set[int] = field(default_factory=set)
            null_value: Optional[str] = None
            empty_nested_list: List[List[int]] = field(default_factory=lambda: [])
            
        empty = EmptyCollections()
        
        jsdc_dump(empty, self.temp_path)
        loaded_empty = jsdc_load(self.temp_path, EmptyCollections)
        
        self.assertEqual(loaded_empty.empty_list, [])
        self.assertEqual(loaded_empty.empty_dict, {})
        self.assertEqual(loaded_empty.empty_set, set())
        self.assertIsNone(loaded_empty.null_value)
        self.assertEqual(loaded_empty.empty_nested_list, [])
        
    def test_inheritance(self):
        """Test serialization/deserialization with inheritance."""
        # 杂鱼♡～继承关系也要测试喵～本喵真是无所不能～
        @dataclass
        class BaseConfig:
            name: str = "base"
            version: str = "1.0.0"
            
        @dataclass
        class DerivedConfig(BaseConfig):
            name: str = "derived"  # 覆盖基类字段
            extra_field: str = "extra"
            
        @dataclass
        class Container:
            base: BaseConfig = field(default_factory=lambda: BaseConfig())
            derived: DerivedConfig = field(default_factory=lambda: DerivedConfig())
            
        container = Container()
        container.base.version = "2.0.0"
        container.derived.extra_field = "custom_value"
        
        jsdc_dump(container, self.temp_path)
        loaded_container = jsdc_load(self.temp_path, Container)
        
        # 验证基类和派生类的字段
        self.assertEqual(loaded_container.base.name, "base")
        self.assertEqual(loaded_container.base.version, "2.0.0")
        self.assertEqual(loaded_container.derived.name, "derived")
        self.assertEqual(loaded_container.derived.version, "1.0.0")
        self.assertEqual(loaded_container.derived.extra_field, "custom_value")
        
    def test_union_types(self):
        """Test serialization/deserialization with Union types."""
        # 杂鱼♡～本喵要测试联合类型了喵～这可是个难点呢～让杂鱼见识一下本喵的厉害～
        @dataclass
        class ConfigWithUnions:
            int_or_str: Union[int, str] = 42
            dict_or_list: Union[Dict[str, int], List[int]] = field(default_factory=lambda: {'a': 1})
            
        # 测试不同的联合类型值
        config1 = ConfigWithUnions(int_or_str=42, dict_or_list={'a': 1, 'b': 2})
        config2 = ConfigWithUnions(int_or_str="string_value", dict_or_list=[1, 2, 3])
        
        # 序列化和反序列化第一个配置
        jsdc_dump(config1, self.temp_path)
        loaded_config1 = jsdc_load(self.temp_path, ConfigWithUnions)
        
        self.assertEqual(loaded_config1.int_or_str, 42)
        self.assertEqual(loaded_config1.dict_or_list, {'a': 1, 'b': 2})
        
        # 序列化和反序列化第二个配置
        jsdc_dump(config2, self.temp_path)
        loaded_config2 = jsdc_load(self.temp_path, ConfigWithUnions)
        
        self.assertEqual(loaded_config2.int_or_str, "string_value")
        self.assertEqual(loaded_config2.dict_or_list, [1, 2, 3])
        
    def test_tuple_types(self):
        """Test serialization/deserialization with tuple types."""
        # 杂鱼♡～本喵要测试元组类型了喵～这种不可变序列也要正确处理才行～
        @dataclass
        class ConfigWithTuples:
            simple_tuple: Tuple[int, str, bool] = field(default_factory=lambda: (1, "test", True))
            int_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))
            empty_tuple: Tuple = field(default_factory=tuple)
            nested_tuple: Tuple[Tuple[int, int], Tuple[str, str]] = field(
                default_factory=lambda: ((1, 2), ("a", "b"))
            )
            
        config = ConfigWithTuples()
        
        jsdc_dump(config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, ConfigWithTuples)
        
        self.assertEqual(loaded_config.simple_tuple, (1, "test", True))
        self.assertEqual(loaded_config.int_tuple, (1, 2, 3))
        self.assertEqual(loaded_config.empty_tuple, ())
        self.assertEqual(loaded_config.nested_tuple, ((1, 2), ("a", "b")))
        
    def test_any_type(self):
        """Test serialization/deserialization with Any type."""
        # 杂鱼♡～本喵现在要测试Any类型了喵～这可是最灵活的类型呢～
        @dataclass
        class ConfigWithAny:
            any_field: Any = None
            any_list: List[Any] = field(default_factory=list)
            any_dict: Dict[str, Any] = field(default_factory=dict)
            
        # 使用各种不同类型的值
        config = ConfigWithAny()
        config.any_field = "string"
        config.any_list = [1, "two", False, None, [1, 2, 3], {"key": "value"}]
        config.any_dict = {
            "int": 42,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        
        jsdc_dump(config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, ConfigWithAny)
        
        self.assertEqual(loaded_config.any_field, "string")
        self.assertEqual(loaded_config.any_list, [1, "two", False, None, [1, 2, 3], {"key": "value"}])
        self.assertEqual(loaded_config.any_dict, {
            "int": 42,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        })
        
    def test_large_json_payload(self):
        """Test serialization/deserialization with large JSON payload."""
        # 杂鱼♡～本喵要测试大型JSON负载了喵～看看杂鱼的程序能不能处理～
        @dataclass
        class LargeDataConfig:
            items: List[Dict[str, Any]] = field(default_factory=list)
            
        # 创建大型数据结构
        large_config = LargeDataConfig()
        for i in range(1000):  # 创建1000个项目
            item = {
                "id": i,
                "name": f"Item {i}",
                "tags": [f"tag{j}" for j in range(10)],  # 每个项目10个标签
                "properties": {f"prop{k}": f"value{k}" for k in range(5)}  # 每个项目5个属性
            }
            large_config.items.append(item)
            
        # 测试序列化和反序列化
        jsdc_dump(large_config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, LargeDataConfig)
        
        # 验证项目数量
        self.assertEqual(len(loaded_config.items), 1000)
        # 验证第一个和最后一个项目
        self.assertEqual(loaded_config.items[0]["id"], 0)
        self.assertEqual(loaded_config.items[999]["id"], 999)
        # 验证结构完整性
        self.assertEqual(len(loaded_config.items[500]["tags"]), 10)
        self.assertEqual(len(loaded_config.items[500]["properties"]), 5)
        
if __name__ == '__main__':
    unittest.main() 