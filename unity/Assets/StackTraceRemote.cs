using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class StackTraceRemote : MonoBehaviour
{


    private static StackTraceRemote _instance;


    private void Awake()
    {
        if (_instance == null)
        {
            _instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            if (_instance != this)
            {
                Destroy(gameObject);
            }
        }

    }

#if UNITY_EDITOR
    [SerializeField]
    private string URI_DEBUG = @"http://localhost:5000/debug/";
#else
    private  string URI_DEBUG = @"http://pacific-beyond-89289.herokuapp.com/debug/";
#endif

    private void Start()
    {
#if UNITY_EDITOR
        LogCallback("Test Condition", "Test Stacktrace", LogType.Log);
#endif
    }
    private void OnEnable()
    {
        Application.logMessageReceived += LogCallback;
    }

    //Called when there is an exception
    private void LogCallback(string condition, string stackTrace, LogType type)
    {
        LogData log = new LogData(condition, stackTrace, type);
        string json_log = JsonUtility.ToJson(log);
        Dictionary<string, string> headers = new Dictionary<string, string>();
        headers["Content-Type"] = "application/json";
        WWW www = new WWW(URI_DEBUG, System.Text.ASCIIEncoding.UTF8.GetBytes(json_log), headers);
    }

    private void OnDisable()
    {
        Application.logMessageReceived -= LogCallback;
    }
}

[System.Serializable]
public class LogData
{
    public string device;
    public string condition;
    public string stackTrace;
    public LogType type;

    public LogData(string condition, string stackTrace, LogType type)
    {
        device = SystemInfo.deviceUniqueIdentifier;
        this.condition = condition;
        this.stackTrace = stackTrace;
        this.type = type;
    }
}