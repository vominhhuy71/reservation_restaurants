using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace ResUI
{
    class Auth
    {
        public string hashSHA256(string rawString)
        {
            SHA256 sHA256 = SHA256.Create();
            byte[] bytes = sHA256.ComputeHash(Encoding.UTF8.GetBytes(rawString));
            // Convert byte array to a string   
            StringBuilder builder = new StringBuilder();
            for (int i = 0; i < bytes.Length; i++)
            {
                builder.Append(bytes[i].ToString("x2"));
            }
            return builder.ToString();
        }
    }
}
