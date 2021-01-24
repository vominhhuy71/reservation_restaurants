using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Text.RegularExpressions;
using System.Net.Http;
using Newtonsoft.Json;
using System.Security.Cryptography;
using Newtonsoft.Json.Linq;

namespace ResUI
{
    /// <summary>
    /// Interaction logic for Login.xaml
    /// </summary>
    public partial class Login : Window
    {
        public Login()
        {
            InitializeComponent();
            errormessage.Visibility = Visibility.Hidden;
        }
        private async void Button_Click(object sender, RoutedEventArgs e)
        {

            if (username.Text.Length == 0)
            {
                errormessage.Visibility = Visibility.Visible;
                errormessage.Text = "Enter an email.";
                username.Focus();
            }
            else if (!Regex.IsMatch(username.Text, "^[a-zA-Z0-9]*$"))
            {
                errormessage.Text = "Enter a valid email.";
                errormessage.Visibility = Visibility.Visible;
                username.Select(0, username.Text.Length);
                username.Focus();
            }
            else
            {
               
                HttpClient client = new HttpClient();                

                HttpResponseMessage nonce_response = await client.GetAsync($"http://localhost:5000/restrv1/login/get_nonce/{username.Text}");
                nonce_response.EnsureSuccessStatusCode();
                string responseString = await nonce_response.Content.ReadAsStringAsync();

                JObject nonceResponse = JObject.Parse(responseString);
                string nonce = nonceResponse.SelectToken("nonce").ToString();

                //Client nonce
                string cnonce = Guid.NewGuid().ToString("N");
             
                Auth auth = new Auth();

                string salt = "_76dwDOPNiui";

                //hash plain text password then add salt
                string hashString = auth.hashSHA256(password.Password+salt) + cnonce + nonce;

                Request_login request = new Request_login();
                request.username = username.Text;
                request.cnonce = cnonce;

                //hash it again
                request.hash = auth.hashSHA256(hashString);

                string output = JsonConvert.SerializeObject(request);
                var httpContent = new StringContent(output, Encoding.UTF8, "application/json");
                HttpResponseMessage response = client.PutAsync("http://localhost:5000/restrv1/login", content: httpContent).Result;
                string resNameString = await response.Content.ReadAsStringAsync();      
                if (response.IsSuccessStatusCode)
                {
                    JObject resnameResponse = JObject.Parse(resNameString);
                    string resName = resnameResponse.SelectToken("name").ToString();
                    string token = resnameResponse.SelectToken("token").ToString();
                    this.Close();
                    MainWindow mainWindow = new MainWindow(resName,token);
                    mainWindow.ShowDialog();
                }
                else
                {
                    errormessage.Visibility = Visibility.Visible;
                    errormessage.Text = "Invalid username/password!";
                }
                
            }
            
        }
    }
}
