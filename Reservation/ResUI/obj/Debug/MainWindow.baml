   M S B A M L   `   `   `  ����@  <ResUI, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullclr-namespace:ResUIResUI  5   	       ResUI.MainWindow   5   	   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   %localclr-namespace:ResUI     5   	     � Title$  
MainWindow��5   	   $	��450��6   $��790.403��6)    � 	Resources 5
       �� 
TargetType �� Property �� Value��%T   '��       �� 5   
   " ��6   .�5      ��  � ��$
 Left=�6;   5      5      .��5      � .+�5   
   �� -   5        $��15(�5      $
��Left=�6#   $	��366��6>   $��	10,54,0,0q�6K   $	��Top=�6^   $	��774��6v   .@�5      �� -   5        $��Reservation��5   +   $��Reservation��6   .��5      � ���	#FFE5E5E5 � ColumnDefinitions 5      �� 5      .+�5      �� -   5         ��Name$ 
lvBookings��5      $��Stretch=�63   $	��232��6Q   $��15,51,4.8,0q�6^   $	��Top=�6s   $	��749��6�   $ �� IsSynchronizedWithCurrentItem$ FalseY�6�    � Cursor$
 Hand��6�   	 �� View	 5      �� 5      .P�5   "   �� $
��Name��61   
 �� Width$	
 200��6?    �� DisplayMemberBinding 6K   �� *
customer+�� 5   "   $��Timeslot��61   $	
 150��6C    6O   �� *
timeslot+�� 5   "   $��Seat(s)��61   $
 75��6B    6M   �� *seats+5      5      �� 5      $/��)The upcoming reservation will come here. ��6   $
��Left=�6P   $��38��6k   $��10,8,0,0q�6w   $	��Top=�6�   $	��749��6�   �� 5       -   5        $��Remove��5       $
��Left=�6.   $��604,288,0,0q�6I   $	��Top=�6^   $��92��6v   $��39��6�   6�   5!      5"      �� 5#      -   5        $��	Available��5#   f   $��	Available��6   $
��Left=�6)   $��0.2,0,-44.4,0q�6D   $��93��6[   .��5$      � ���	#FFE5E5E5.+�5%      �� $��0q�6   $
��Left=�60   $��27��6K   $��
0,0,-3.2,0q�6W   $2��,Add, remove or check status for reservation.��6k   $	��Top=�6�   $	��772��6�   �� 5'      -   5        $��Add time��5'      $
��Left=�60   $��41��6K   $��612,284,0,0q�6W   $	��Top=�6l   $	��147��6�   6�   �� 5(      -   5        $��Remove��5(      $
��Left=�6.   $��41��6I   $��
10,284,0,0q�6U   $	��Top=�6i   $	��147��6�   6�   �� 5)      -   5        $ lvSlots��5)   -   $
 Hand��6   $
��Left=�6>   $	��234��6Y   $��	10,32,0,0q�6f   $	��Top=�6y   $	��746��6�   	 5*      �� 5+      .P�5,   "   �� $��Timeslot��61   $	
 300��6C    6O   �� *
timeslot+�� 5-   "   $��	Available��61   $	
 200��6D    6P   �� *	available+5.      50      51      52      54      �� 56   
   -	   5        $��ResName��56   r   $��Restaurant name here��6   $
��Left=�6.   $��10,10,0,366q�6I    �� TextWrapping$
 Wrap=�6^   $��0q�6�    �� 
IsReadOnly . $	��774��6�   $
��25px(�6�   58      59      