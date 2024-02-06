# PASSNAGER 🔐
#### Video Demo: https://youtu.be/aGZUYIa5y2U
#### Description: 
![image](https://github.com/hng011/passnager/assets/93465725/4d5b3f6b-8632-4d76-a2e2-e3a76d3ee8fa)

Passnager is a simple command-line based program to save your passwords safely in a csv file. it utilizes an encryption technique to protect the data stored within the csv file. If you're not that good in remebering your own passwords. Passnager can be a valuable tool. It keeps your password accessible and secure. In fact, if you can easily remember your own passwords, that means your passwords are not strong enough or you're just an extraordinary human-being that truly have an exceptional memory, for your sake, please consider to change them and store it into Passnager!!!. 

## HOW TO USE 🧐
1. Clone the repository
   ```bash
   git clone https://github.com/hng011/passnager.git
   ```
2. Install packages
   ```bash
   pip install -r requirements.txt
   ```
3. Create a .env file
   - Firstly, you can copy the .env.example file and paste it into the root of the project folder
     <br/>![image](https://github.com/hng011/passnager/assets/93465725/9329fd66-0cfe-44d9-8399-e8cd79c8f79a)

   - Then rename the file that you paste with .env
     <br/>![image](https://github.com/hng011/passnager/assets/93465725/58d00cd2-7796-490d-ad31-ffc5ee4d5d28)

     
4. Generate a secret key
   ```bash
   python project.py --generate-key
   ```
   
5. Finally you can run the program normally
   ```bash
   python project.py
   ```
