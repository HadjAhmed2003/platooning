using System;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Windows.Forms;
using SCSSdkClient;
using SCSSdkClient.Object;
using System.Data.SqlClient;


namespace ConsoleApp1
{
    class Program
    {
        //static SqlConnection conn = new SqlConnection();
        static int count = 0;
        static void Main(string[] args)
        {
            //conn.ConnectionString =
            //"Data Source=.\\SQLExpress;" +
            //"Initial Catalog = truck-platooning-ATR;" +
            //"Trusted_Connection = true;"+
            //"User id=DESKTOP-PV4B6HF\\AUC;";
            //conn.Open();
            StreamReader sr = new StreamReader("C:\\Users\\ATR Lab\\Desktop\\platooning\\truck-telemtry\\count.txt");
            //Read the first line of text
            count = Int32.Parse(sr.ReadLine());
            sr.Close();
            var path = @"C:\Users\ATR Lab\Desktop\platooning\data.csv";
            if (!File.Exists(path))
            {
                var w = new StreamWriter(path, true);
                var line =
                    "System_Date," +
                    "System_Time," +
                    "Telemetry_Timestamp," +
                    "Simulation_Timestamp," +
                    "Electric_Enabled," +
                    "Engine_Enabled," +
                    "LiftAxle," +
                    "LiftAxleIndicator," +
                    "TrailerLiftAxle," +
                    "TrailerLiftAxleIndicator," +
                    "HShifterSlot," +
                    "Selected," +
                    "HShiftSelector," +
                    "RetarderLevel," +
                    "Air_Pressure," +
                    "Temperature," +
                    "Parking_Brake," +
                    "Motor_Brake," +
                    "Damage_Engine," +
                    "Damage_Transmission," +
                    "Damage_Cabin," +
                    "Damage_Chassis," +
                    "Damage_Wheels," +
                    "UserInput_Steering," +
                    "UserInput_Throttle," +
                    "UserInput_Brake," +
                    "UserInput_Clutch," +
                    "Speed," +
                    "RPM," +
                    "image_path," +
                    "Pygame_Left_Y," +
                    "Pygame_Left_X," +
                    "Pygame_Right_Y," +
                    "Pygame_Right_X";
                w.WriteLine(line);
                w.Flush();
                w.Close();
            }
            SCSSdkTelemetry Telemetry = new SCSSdkTelemetry();
            Telemetry.Data += Telemetry_Data;
            if (Telemetry.Error != null)
            {
                // Error connection to the memory map
            }
            // do not close the program until `q` was typed 
            if (Console.ReadKey(true).KeyChar == 'q')
            {
                StreamWriter sw = new StreamWriter("C:\\Users\\ATR Lab\\Desktop\\platooning\\truck-telemtry\\count.txt");
                //Write a line of text
                sw.WriteLine(count.ToString());
                //Close the file
                sw.Close();
                return;     
            }
        }


        private static void Telemetry_Data(SCSTelemetry data, bool updated)
        {
            try
            {
                
                var SystemTime = DateTime.Now.ToString("HH:mm:ss.ffffff");
                var systemDate = DateTime.Now.ToString("d");
                var img_path = string.Format("\"C:/Users/ATR Lab/Desktop/platooning/screenshots/{0}.png\"", count);
                System.Diagnostics.Process process = new System.Diagnostics.Process();
                System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
                startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
                startInfo.FileName = "cmd.exe";
                startInfo.Arguments = "/C python \"C:\\Users\\ATR Lab\\Desktop\\platooning\\test.py\" " + img_path;
                
                startInfo.RedirectStandardOutput= true;
                process.StartInfo = startInfo;
                process.Start();
                string pygame_inputs = process.StandardOutput.ReadToEnd();
                //Console.WriteLine("from C#: " + pygame_inputs);
                var path = @"C:\Users\ATR Lab\Desktop\platooning\data.csv";
                using (var w = new StreamWriter(path, true))
                {
                    var line = string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24},{25},{26},{27},{28},{29},{30}",
                            systemDate,
                            SystemTime,
                            data.Timestamp,
                            (data.SimulationTimestamp / Math.Pow(10, 6)),
                            data.TruckValues.CurrentValues.ElectricEnabled,
                            data.TruckValues.CurrentValues.EngineEnabled,
                            data.TruckValues.CurrentValues.LiftAxle,
                            data.TruckValues.CurrentValues.LiftAxleIndicator,
                            data.TruckValues.CurrentValues.TrailerLiftAxle,
                            data.TruckValues.CurrentValues.TrailerLiftAxleIndicator,
                            data.TruckValues.CurrentValues.MotorValues.GearValues.HShifterSlot,
                            data.TruckValues.CurrentValues.MotorValues.GearValues.Selected,
                            data.TruckValues.CurrentValues.MotorValues.GearValues.HShifterSelector,
                            data.TruckValues.CurrentValues.MotorValues.BrakeValues.RetarderLevel,
                            data.TruckValues.CurrentValues.MotorValues.BrakeValues.AirPressure,
                            data.TruckValues.CurrentValues.MotorValues.BrakeValues.Temperature,
                            data.TruckValues.CurrentValues.MotorValues.BrakeValues.ParkingBrake,
                            data.TruckValues.CurrentValues.MotorValues.BrakeValues.MotorBrake,
                            data.TruckValues.CurrentValues.DamageValues.Engine,
                            data.TruckValues.CurrentValues.DamageValues.Transmission,
                            data.TruckValues.CurrentValues.DamageValues.Cabin,
                            data.TruckValues.CurrentValues.DamageValues.Chassis,
                            data.TruckValues.CurrentValues.DamageValues.WheelsAvg,
                            data.ControlValues.InputValues.Steering,
                            data.ControlValues.InputValues.Throttle,
                            data.ControlValues.InputValues.Brake,
                            data.ControlValues.InputValues.Clutch,
                            data.TruckValues.CurrentValues.DashboardValues.Speed.Kph,
                            data.TruckValues.CurrentValues.DashboardValues.RPM,
                            img_path,
                            pygame_inputs) ;

                    w.WriteLine(line);
                    w.Flush(); w.Close();
                    count++;
                }
                //SqlCommand command1 = new SqlCommand(string.Format("insert into dbo.game_values values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}')",
                //    systemDate,
                //    SystemTime,
                //    data.Timestamp,
                //    (data.SimulationTimestamp / Math.Pow(10, 6)),
                //    data.TruckValues.CurrentValues.ElectricEnabled,
                //    data.TruckValues.CurrentValues.EngineEnabled,
                //    data.TruckValues.CurrentValues.LiftAxle,
                //    data.TruckValues.CurrentValues.LiftAxleIndicator,
                //    data.TruckValues.CurrentValues.TrailerLiftAxle,
                //    data.TruckValues.CurrentValues.TrailerLiftAxleIndicator,
                //    data.TruckValues.CurrentValues.MotorValues.GearValues.HShifterSlot,
                //    data.TruckValues.CurrentValues.MotorValues.GearValues.Selected,
                //    data.TruckValues.CurrentValues.MotorValues.GearValues.HShifterSelector,
                //    data.TruckValues.CurrentValues.MotorValues.BrakeValues.RetarderLevel,
                //    data.TruckValues.CurrentValues.MotorValues.BrakeValues.AirPressure,
                //    data.TruckValues.CurrentValues.MotorValues.BrakeValues.Temperature,
                //    data.TruckValues.CurrentValues.MotorValues.BrakeValues.ParkingBrake,
                //    data.TruckValues.CurrentValues.MotorValues.BrakeValues.MotorBrake,
                //    data.TruckValues.CurrentValues.DamageValues.Engine,
                //    data.TruckValues.CurrentValues.DamageValues.Transmission,
                //    data.TruckValues.CurrentValues.DamageValues.Cabin,
                //    data.TruckValues.CurrentValues.DamageValues.Chassis,
                //    data.TruckValues.CurrentValues.DamageValues.WheelsAvg,
                //    data.ControlValues.InputValues.Steering,
                //    data.ControlValues.InputValues.Throttle,
                //    data.ControlValues.InputValues.Brake,
                //    data.ControlValues.InputValues.Clutch,
                //    data.TruckValues.CurrentValues.DashboardValues.Speed.Kph,
                //    data.TruckValues.CurrentValues.DashboardValues.RPM
                //    ), conn);
                //command1.ExecuteNonQuery();
                //SqlCommand command2 = new SqlCommand(string.Format("insert into dbo.screenshots values('{0}','{1}','{2}')",
                //    systemDate, SystemTime, img_path), conn);
                //command2.ExecuteNonQuery();
                //string[] splitted = pygame_inputs.Split(',');
                //SqlCommand command3 = new SqlCommand(string.Format("insert into dbo.pygame_inputs values('{0}','{1}','{2}','{3}','{4}','{5}')",
                //    systemDate, SystemTime, splitted[0], splitted[1], splitted[2], splitted[3]), conn);
                //command3.ExecuteNonQuery();

            }
            catch (Exception ex)
            {
            }
        }

    }
}
