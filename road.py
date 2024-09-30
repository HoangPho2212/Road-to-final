import tkinter as tk
from tkinter import messagebox


teams = ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F", "Team G", "Team H"]

# Số lần thua của mỗi đội
team_losses = {team: 0 for team in teams}


winners_bracket_matches = []
losers_bracket_matches = []


finals = []

root = tk.Tk()
root.title("Double Elimination Tournament")


match_index = 0

# Lịch thi đấu cho 8 đội (tổng 13 trận)
matches_schedule = [
    # Vòng đầu tiên của nhánh thắng
    ("Team A", "Team B"),
    ("Team C", "Team D"), 
    ("Team E", "Team F"), 
    ("Team G", "Team H"),

    # Vòng 2 - Nhánh thắng và nhánh thua
    ("Winner 1", "Winner 2"), 
    ("Winner 3", "Winner 4"), 
    ("Loser 1", "Loser 2"), 
    ("Loser 3", "Loser 4"),

    # Vòng 3 - Nhánh thắng, nhánh thua tiếp tục
    ("Winner 5", "Winner 6"), 
    ("Winner 7", "Winner 8"), 

    # Vòng 4 - Nhánh thua & quyết định trận chung kết
    ("Loser 5", "Loser 6"), 
    ("Winner 9", "Winner 10"),

    # Trận chung kết
    ("Winner 11", "Loser 10")
]

# Hàm xử lý khi người dùng nhập kết quả
def enter_result():
    global match_index
    
    if match_index >= len(matches_schedule):
        messagebox.showinfo("Thông báo", "Giải đấu đã kết thúc!")
        return
    
    team1 = team1_var.get()
    team2 = team2_var.get()
    winner = winner_var.get()
    
    if winner not in [team1, team2]:
        messagebox.showerror("Lỗi", "Đội thắng không hợp lệ!")
        return

    loser = team1 if winner == team2 else team2
    process_result(winner, loser)
    
    match_index += 1
    if match_index < len(matches_schedule):
        next_match()

# Xử lý kết quả của trận đấu
def process_result(winner, loser):
    team_losses[loser] += 1
    if team_losses[loser] == 2:
        messagebox.showinfo("Bị loại", f"Đội {loser} đã bị loại khỏi giải đấu.")
    
    update_brackets(winner, loser)

def update_brackets(winner, loser):
    global winners_bracket_matches, losers_bracket_matches
    
    if match_index < 4:  # Vòng nhánh thắng đầu tiên
        winners_bracket_matches.append(winner)
    else:  # Các vòng nhánh thua
        losers_bracket_matches.append(loser)
        
    if match_index == 12:  # Trận chung kết
        show_final_results()


def next_match():
    match = matches_schedule[match_index]
    match_label.config(text=f"Trận đấu: {match[0]} vs {match[1]}")
    team1_var.set(match[0])
    team2_var.set(match[1])
    team1_radio.config(value=match[0])
    team2_radio.config(value=match[1])
    winner_var.set("")

def show_final_results():
    champion = winners_bracket_matches[-1]
    runner_up = losers_bracket_matches[-1]
    
    # Giải ba là 2 đội thua trận gần cuối cùng ở nhánh thua
    third_place = [losers_bracket_matches[-2], losers_bracket_matches[-3]]
    
    messagebox.showinfo("Kết quả", f"Đội vô địch là: {champion}\n"
                                   f"Giải nhì: {runner_up}\n"
                                   f"Giải ba: {third_place[0]}, {third_place[1]}")
    root.quit()

# Các biến lưu trữ thông tin trận đấu
team1_var = tk.StringVar()
team2_var = tk.StringVar()
winner_var = tk.StringVar()

# Nhãn hiển thị trận đấu hiện tại
match_label = tk.Label(root, text="", font=("Arial", 16))
match_label.pack(pady=20)

# Lựa chọn đội thắng
team1_radio = tk.Radiobutton(root, textvariable=team1_var, variable=winner_var)
team1_radio.pack()

team2_radio = tk.Radiobutton(root, textvariable=team2_var, variable=winner_var)
team2_radio.pack()

# Nút để xác nhận kết quả
submit_button = tk.Button(root, text="Xác nhận kết quả", command=enter_result)
submit_button.pack(pady=20)


next_match()

root.mainloop()
