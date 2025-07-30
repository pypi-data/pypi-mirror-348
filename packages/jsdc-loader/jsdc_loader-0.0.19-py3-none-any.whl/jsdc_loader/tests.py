"""Test cases for JSDC Loader."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict, Set
import tempfile
import os
import unittest

from pydantic import BaseModel

from .loader import jsdc_load, jsdc_loads
from .dumper import jsdc_dump

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

if __name__ == '__main__':
    unittest.main() 