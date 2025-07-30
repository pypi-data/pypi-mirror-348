# Test all OfficeMCP tools
import officemcp.OfficeMCP as OfficeMCP

print("=== OfficeMCP Comprehensive Testing ===")

try:
    path = OfficeMCP.ScreenShot()
    print("ScreeShoted successfully: {path}")
    path = OfficeMCP.ScreenShot('My.png')
    print("ScreeShoted successfully: {path}")
    path = OfficeMCP.DownloadImage()
    print("ScreeShoted successfully: {path}")  
    # Test application lifecycle tools
    print("[3/5] Testing AvailableApplications...")
    apps = OfficeMCP.AvailableApps()
    print(f"Installed apps: {', '.join(apps)}")

    print("[4/6] Testing IsAppAvailable...")
    assert OfficeMCP.IsAppAvailable("Excel"), "Excel should be available"
    assert not OfficeMCP.IsAppAvailable("FakeApp"), "FakeApp should not be available"

    print("\n[1/5] Testing Launch...")
    assert OfficeMCP.Launch("Excel"), "Failed to launch Excel"
    
    print("\n[2/5] Testing Visible...")
    assert OfficeMCP.Visible("Excel", True), "Failed to make Excel visible"   

    print("\n[1/5] running apps...")
    for app in OfficeMCP.RunningApps():
        print(f"Running app: {app}")

    print("[4/5] Testing Quit...")
    assert OfficeMCP.Quit("Excel"), "Failed to quit Excel"   
    
    print("[5/5] Testing RunPython...")
    codes = '''
Officer.Excel.Visible = True
Officer.Excel.Workbooks.Add()
Officer.Excel.ActiveSheet.Cells(1,1).Value = "Test RunPython Tool Successful"
'''
    result = OfficeMCP.RunPython(codes)
    assert result['success'], f"Python execution failed: {result.get('error', '')}"

    print("[7/7] Testing Demonstrate...")
    OfficeMCP.Demonstrate()

    print("\nAll non-demonstration tests completed successfully!")

except Exception as e:
    print(f"\nTest failed: {str(e)}")

