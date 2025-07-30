from datetime import datetime
from multiprocessing import Lock, Queue
from pyedflib import FILETYPE_BDFPLUS, FILETYPE_EDFPLUS, EdfWriter
from threading import Thread
from loguru import logger
import numpy as np
import os

class EDFWriterThread(Thread):
    def __init__(self, edf_writer : EdfWriter):
        super().__init__(self)
        self._edf_writer : EdfWriter = edf_writer
        self.data_queue : Queue = Queue()
        self._stop_event : bool = False
        self._recording = False
        self._chunk = np.array([])
        self._points = 0
        self._duration = 0
        self._sample_frequency = 0
        self._total_packets = 0
        self._channels = []
        self._sample_rate = 0
        
    def start(self):
        self._stop_event = False
        super().start()
        
    def stop(self):
        self._stop_event = True
        
    def append(self, data):
        # 数据
        self.data_queue.put(data)
        
    def _consumer(self):
        logger.debug(f"开始消费数据 _consumer: {self.data_queue.qsize()}")
        while True:
            if self._recording or (not self.data_queue.empty()):
                try:
                    data = self.data_queue.get(timeout=10)
                    if data is None:
                        break
                    # 处理数据
                    self._points += len(data)
                    self._write_file(data)
                except Exception as e:
                    logger.error("数据队列为空，超时(10s)结束")
                    break
            else:
                break
            
        self.close()
        
    def _write_file(self, eeg_data):
        try:            
            if (self._chunk.size == 0):
                self._chunk = np.asarray(eeg_data)
            else:                
                self._chunk = np.hstack((self._chunk, eeg_data))
                
            if self._chunk.size >= self._sample_rate * self._channels:                
                self._write_chunk(self._chunk[:self._sample_rate])
                self._chunk = self._chunk[self._sample_rate:]            
            
        except Exception as e:
            logger.error(f"写入数据异常: {str(e)}")
        
    def close(self):
        self._recording = False
        if self._edf_writer:            
            self._end_time = datetime.now().timestamp()
            self._edf_writer.writeAnnotation(0, 1, "start recording ")
            self._edf_writer.writeAnnotation(self._duration, 1, "recording end")
            self._edf_writer.close()
        
        logger.info(f"文件: {self.file_name}完成记录, 总点数: {self._points}, 总时长: {self._duration}秒 丢包数: {self._lost_packets}/{self._total_packets + self._lost_packets}")
        
    
        
    def _write_chunk(self, chunk):
        logger.debug(f"写入数据: {chunk}")
        # 转换数据类型为float64（pyedflib要求）
        data_float64 = chunk.astype(np.float64)
        # 写入时转置为(样本数, 通道数)格式
        self._edf_writer.writeSamples(data_float64)
        self._duration += 1

class RscEDFHandler(object):
    '''
        Rsc EDF Handler
        处理EDF文件的读写
        RSC设备通道数根据选择变化，不同通道采样频率相同
        sample_frequency: 采样频率
        physical_max: 物理最大值    
        physical_min: 物理最小值
        digital_max: 数字最大值
        digital_min: 数字最小值
        resolution: 分辨率
        storage_path: 存储路径        
        
        @author: qlsdk
        @since: 0.4.0
    '''
    def __init__(self, sample_frequency, physical_max, physical_min, digital_max, digital_min, resolution=32, storage_path = None):
        # edf文件参数
        self.physical_max = physical_max
        self.physical_min = physical_min
        self.digital_max = digital_max
        self.digital_min = digital_min
        # 点分辨率
        self.resolution = resolution
        # eeg通道数
        self.eeg_channels = None
        # eeg采样率
        self.eeg_sample_rate = 500
        self.acc_channels = None
        self.acc_sample_rate = 50
        # 缓存
        self._cache = Queue()
        # 采样频率
        self.sample_frequency = sample_frequency
        # bytes per second
        self.bytes_per_second = 0
        self._edf_writer = None
        self._cache2 = tuple()
        self._recording = False
        self._edf_writer = None
        self.annotations = None
        # 每个数据块大小
        self._chunk = np.array([])
        self._Lock = Lock()
        self._duration = 0
        self._points = 0
        self._first_pkg_id = None
        self._last_pkg_id = None
        self._first_timestamp = None
        self._end_time = None
        self._patient_code = "patient_code"
        self._patient_name = "patient_name"
        self._device_type = None
        self._total_packets = 0
        self._lost_packets = 0
        self._storage_path = storage_path
        self._edf_writer_thread = None
        
    @property
    def file_name(self): 
        if self._storage_path:
            try:
                os.makedirs(self._storage_path, exist_ok=True)  # 自动创建目录，存在则忽略
                return f"{self._storage_path}/{self._device_type}_{self._first_timestamp}.edf"
            except Exception as e:
                logger.error(f"创建目录[{self._storage_path}]失败: {e}")
            
        return f"{self._device_type}_{self._first_timestamp}.edf"
         
    @property
    def file_type(self):
        return FILETYPE_BDFPLUS if self.resolution == 24 else FILETYPE_EDFPLUS
    
    def set_device_type(self, device_type):
        self._device_type = device_type
        
    def set_storage_path(self, storage_path):
        self._storage_path = storage_path
        
    def set_patient_code(self, patient_code):
        self._patient_code = patient_code
        
    def set_patient_name(self, patient_name):
        self._patient_name = patient_name
    
    def append(self, data, channels=None):
        if self._edf_writer_thread is None:
            self._edf_writer_thread = EDFWriterThread(self.init_edf_writer())
            self._edf_writer_thread.start()
            self._recording = True
            self._edf_writer_thread._recording = True
            logger.info(f"开始写入数据: {self.file_name}")
            
        if data:
            # # 通道数
            # if self._first_pkg_id is None:
            #     self.eeg_channels = data.eeg_ch_count
            #     self.acc_channels = data.acc_ch_count
            #     self._first_pkg_id = data.pkg_id
            #     self._first_timestamp = data.time_stamp
                
            # if self._last_pkg_id and self._last_pkg_id != data.pkg_id - 1:  
            #     self._lost_packets += data.pkg_id - self._last_pkg_id - 1
            #     logger.warning(f"数据包丢失: {self._last_pkg_id} -> {data.pkg_id}, 丢包数: {data.pkg_id - self._last_pkg_id - 1}")
                
            self._last_pkg_id = data.pkg_id
            self._total_packets += 1
            
        # 数据
        self._cache.put(data)
        self._edf_writer_thread.append(data)
        # if not self._recording:
        #     self.start()
    
    def trigger(self, data):
        pass        
        
    def init_edf_writer(self):
        # 创建EDF+写入器
        edf_writer = EdfWriter(
            self.file_name,
            self.eeg_channels,
            file_type=self.file_type
        )
        
        # 设置头信息
        edf_writer.setPatientCode(self._patient_code)
        edf_writer.setPatientName(self._patient_name)
        edf_writer.setEquipment(self._device_type)
        edf_writer.setStartdatetime(datetime.now())
        
        # 配置通道参数
        signal_headers = []
        for ch in range(self.eeg_channels):
            signal_headers.append({
                "label": f'channels {ch + 1}',
                "dimension": 'uV',
                "sample_frequency": self.sample_frequency,
                "physical_min": self.physical_min,
                "physical_max": self.physical_max,
                "digital_min": self.digital_min,
                "digital_max": self.digital_max
            })
        
        edf_writer.setSignalHeaders(signal_headers)
        
        return edf_writer

    